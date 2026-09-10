"""PyTorch models for the comparison: MLP (tabular), 1D-CNN and GRU (sequence),
and CNN/GRU hybrids that also see the hand-crafted features.

All are trained **program-batched**: a batch is a set of programs; each program's
representation is encoded once and scored against all 64 pass combos in one
forward pass.  On CPU the row-batched alternative (57k rows) is ~50x slower.
"""
import numpy as np
import torch
import torch.nn as nn

from .dataset import FLAG_BITS
from .sequences import PAD, VOCAB_SIZE

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NUM_COMBOS = 64
_ALL_BITS = torch.tensor(
    [[1.0 if c & b else 0.0 for b in FLAG_BITS] for c in range(NUM_COMBOS)],
    dtype=torch.float32)  # (64, 6)

H = 96  # program-embedding width shared by every encoder


class _MLPEnc(nn.Module):
    def __init__(self, n_feat):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_feat, 128), nn.ReLU(), nn.Dropout(0.1),
            nn.Linear(128, H), nn.ReLU())

    def forward(self, feats, tokens=None):
        return self.net(feats)


class _CNNEnc(nn.Module):
    def __init__(self, emb=32):
        super().__init__()
        self.emb = nn.Embedding(VOCAB_SIZE, emb, padding_idx=PAD)
        self.conv = nn.Sequential(
            nn.Conv1d(emb, 64, 5, padding=2), nn.ReLU(),
            nn.Conv1d(64, 64, 5, padding=2), nn.ReLU(),
            nn.Conv1d(64, 128, 5, padding=2), nn.ReLU())
        self.proj = nn.Linear(128, H)

    def forward(self, feats, tokens):
        x = self.emb(tokens).transpose(1, 2)   # (B, emb, L)
        x = self.conv(x).amax(dim=2)           # (B, 128) global max-pool
        return torch.relu(self.proj(x))


class _GRUEnc(nn.Module):
    """1-layer GRU over packed (padding-skipped) sequences.  Deliberately compact
    -- an RNN on 640-token programs on CPU is the slowest model here; a larger /
    bidirectional GRU would need a GPU (noted as a limitation)."""

    GRU_CAP = 320

    def __init__(self, emb=24, hid=48):
        super().__init__()
        self.emb = nn.Embedding(VOCAB_SIZE, emb, padding_idx=PAD)
        self.gru = nn.GRU(emb, hid, num_layers=1, batch_first=True)
        self.proj = nn.Linear(hid, H)

    def forward(self, feats, tokens):
        tokens = tokens[:, :self.GRU_CAP]
        lengths = (tokens != PAD).sum(dim=1).clamp_min(1).cpu()
        packed = nn.utils.rnn.pack_padded_sequence(
            self.emb(tokens), lengths, batch_first=True, enforce_sorted=False)
        _, hn = self.gru(packed)               # hn (1, B, hid)
        return torch.relu(self.proj(hn[-1]))


class _HybridEnc(nn.Module):
    def __init__(self, seq_enc, n_feat):
        super().__init__()
        self.seq = seq_enc
        self.feat = nn.Sequential(nn.Linear(n_feat, 64), nn.ReLU())
        self.merge = nn.Linear(H + 64, H)

    def forward(self, feats, tokens):
        return torch.relu(self.merge(
            torch.cat([self.seq(feats, tokens), self.feat(feats)], dim=-1)))


class _SpeedupNet(nn.Module):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder
        self.head = nn.Sequential(
            nn.Linear(H + 6, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, feats, tokens):
        enc = self.encoder(feats, tokens)              # (B, H)
        B = enc.shape[0]
        bits = _ALL_BITS.to(enc.device)               # (64, 6)
        enc = enc.unsqueeze(1).expand(B, NUM_COMBOS, H)
        bits = bits.unsqueeze(0).expand(B, NUM_COMBOS, 6)
        return self.head(torch.cat([enc, bits], dim=-1)).squeeze(-1)  # (B, 64)


def _build(kind, n_static):
    if kind == "mlp":
        return _SpeedupNet(_MLPEnc(n_static))
    if kind == "cnn1d":
        return _SpeedupNet(_CNNEnc())
    if kind == "gru":
        return _SpeedupNet(_GRUEnc())
    if kind == "cnn1d_hybrid":
        return _SpeedupNet(_HybridEnc(_CNNEnc(), n_static))
    if kind == "gru_hybrid":
        return _SpeedupNet(_HybridEnc(_GRUEnc(), n_static))
    raise ValueError(kind)


class TorchSpeedupModel:
    """sklearn-ish wrapper, program-batched.  fit() takes per-program arrays."""

    # (epochs, patience, batch) per family -- the GRU is the CPU bottleneck
    _CFG = {
        "mlp":          (120, 15, 128),
        "cnn1d":        (60,  10, 96),
        "cnn1d_hybrid": (60,  10, 96),
        "gru":          (30,  6,  128),
        "gru_hybrid":   (30,  6,  128),
    }

    def __init__(self, kind, seed=0, n_static=27, epochs=None, batch=None, lr=1e-3):
        e, p, b = self._CFG.get(kind, (60, 10, 96))
        self.kind = kind
        self.seed = seed
        self.n_static = n_static
        self.epochs = epochs or e
        self.patience = p
        self.batch = batch or b
        self.lr = lr
        self.net = None

    # -- fit ------------------------------------------------------------------ #
    @staticmethod
    def _t(a, dtype):
        return torch.from_numpy(np.ascontiguousarray(a)).to(dtype).to(DEVICE)

    def fit(self, feats, tokens, speedup, mask):
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        self.net = _build(self.kind, self.n_static).to(DEVICE)

        f = self._t(feats, torch.float32)
        t = self._t(tokens, torch.long) if tokens is not None else None
        sp = self._t(speedup, torch.float32)
        mk = self._t(mask, torch.float32)

        P = f.shape[0]
        perm = np.random.permutation(P)
        n_val = max(8, P // 8)
        val, trn = perm[:n_val], perm[n_val:]
        opt = torch.optim.Adam(self.net.parameters(), lr=self.lr, weight_decay=1e-5)

        best_val, best_state, bad = float("inf"), None, 0
        for ep in range(self.epochs):
            self.net.train()
            for s in range(0, len(trn), self.batch):
                b = trn[s:s + self.batch]
                fb = f[b]
                tb = t[b] if t is not None else None
                pred = self.net(fb, tb)
                err = (pred - sp[b]) ** 2 * mk[b]
                loss = err.sum() / mk[b].sum().clamp_min(1)
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.net.parameters(), 5.0)
                opt.step()

            self.net.eval()
            with torch.no_grad():
                vp = self.net(f[val], t[val] if t is not None else None)
                vloss = float(((vp - sp[val]) ** 2 * mk[val]).sum()
                              / mk[val].sum().clamp_min(1))
            if vloss < best_val - 1e-4:
                best_val = vloss
                best_state = {k: v.detach().clone()
                              for k, v in self.net.state_dict().items()}
                bad = 0
            else:
                bad += 1
                if bad >= self.patience:
                    break
        if best_state is not None:
            self.net.load_state_dict(best_state)
        return self

    # -- predict ------------------------------------------------------------- #
    @torch.no_grad()
    def predict(self, feats, tokens):
        self.net.eval()
        f = self._t(feats, torch.float32)
        t = self._t(tokens, torch.long) if tokens is not None else None
        out = []
        for s in range(0, f.shape[0], 128):
            out.append(self.net(f[s:s + 128],
                                t[s:s + 128] if t is not None else None).cpu().numpy())
        return np.concatenate(out, axis=0)  # (n, 64)

    def state_size_kb(self) -> float:
        import io
        buf = io.BytesIO()
        torch.save(self.net.state_dict(), buf)
        return len(buf.getvalue()) / 1024
