"""Pass 6 -- Loop Unrolling.

Under ``gcc -O0`` every loop pays a fixed per-iteration tax: reload the induction
variable, compare, conditional branch, branch back.  Duplicating a small
straight-line body K times amortises that tax over K useful iterations.

Only the simplest, provably safe shape is unrolled -- the one the front end
emits for ``while (iv < CONST) { ... iv = iv + c; ... }``:

    L_head:
        tc = iv < BOUND            (BOUND a constant; LT/LE, or GT/GE for a
        ifFalse tc goto L_end       decreasing loop)
        <BODY>                     straight line: no labels, jumps, returns,
        goto L_head                 and no nested loop
    L_end:

with ``iv`` updated exactly once in the body by a constant step and written
nowhere else.  The transform keeps the *original* loop untouched as the
remainder handler and drops a K-wide copy in front of it:

    L_unroll_k:
        gc = iv <(=) BOUND - (K-1)*c
        ifFalse gc goto L_head          not K full iterations left -> remainder
        <BODY x K>                      (temps renamed per copy)
        goto L_unroll_k
    L_head:  ... original loop ...      handles the last 0..K-1 iterations
    L_end:

Anything that does not match is left exactly as-is.
"""
import copy
from typing import Dict, List, Optional, Set, Tuple

from ..ir.tac import (
    Opcode, TACInstruction, TACFunction, Constant, Var, Temp, Label,
)
from ..ir.cfg import build_cfg_for_function
from ._util import wrap32, const_int_value, op_name, defined_name

UNROLL_FACTOR = 4
MAX_BODY = 28  # instructions; larger bodies gain little and bloat compile time

_CTRL = {Opcode.LABEL, Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE,
         Opcode.RETURN}
_REL_INV = {Opcode.LT: Opcode.LT, Opcode.LE: Opcode.LE,
            Opcode.GT: Opcode.GT, Opcode.GE: Opcode.GE}

_counter = [0]


def _fresh_suffix() -> int:
    _counter[0] += 1
    return _counter[0]


def loop_unroll_pass(func: TACFunction, global_names: frozenset = frozenset()) -> TACFunction:
    out = copy.deepcopy(func)
    done: set = set()          # header labels already unrolled -- never touch again
    for _ in range(16):        # one loop per iteration; re-analyse after each rewrite
        if not _unroll_one(out, done):
            break
    return out


def _unroll_one(func: TACFunction, done: set) -> bool:
    cfg = build_cfg_for_function(func)
    insts = func.instructions

    for loop in sorted(cfg.loops, key=lambda l: l.depth):  # innermost first
        header = loop.header
        if not header.instructions or header.instructions[0].opcode != Opcode.LABEL:
            continue
        head_label_inst = header.instructions[0]
        head_label = str(head_label_inst.dst)
        if head_label in done or _already_unrolled(insts, head_label):
            continue

        try:
            h = next(i for i, ins in enumerate(insts) if ins is head_label_inst)
        except StopIteration:
            continue

        # header must be:  LABEL ; tc = iv REL bound ; ifFalse tc goto END
        if h + 2 >= len(insts):
            continue
        cmp_i, br_i = insts[h + 1], insts[h + 2]
        if cmp_i.opcode not in _REL_INV or br_i.opcode != Opcode.JUMP_IF_FALSE:
            continue
        if op_name(br_i.src1) != op_name(cmp_i.dst):
            continue
        end_label = str(br_i.dst)

        iv, bound_c, rel = _match_iv_bound(cmp_i)
        if iv is None:
            continue

        # find the latch:  goto head_label  that closes this loop
        latch_idx = None
        for k in range(h + 3, len(insts)):
            ins = insts[k]
            if ins.opcode == Opcode.JUMP and str(ins.dst) == head_label:
                latch_idx = k
                break
            if ins.opcode == Opcode.LABEL and str(ins.dst) == end_label:
                break
        if latch_idx is None:
            continue

        body = insts[h + 3:latch_idx]
        if not body or len(body) > MAX_BODY:
            continue
        if any(b.opcode in _CTRL for b in body):
            continue

        step = _single_iv_step(body, iv)
        if step is None or step == 0:
            continue
        if _has_loop_carried_temp(body):
            continue  # a temp read before it is written this iteration is
                      # carried across the back-edge -- duplicating the body
                      # with renamed temps would break it
        # direction must agree with the relation
        if rel in (Opcode.LT, Opcode.LE) and step <= 0:
            continue
        if rel in (Opcode.GT, Opcode.GE) and step >= 0:
            continue
        if _writes_other_than_step(body, iv):
            continue

        # --- build the unrolled prologue -------------------------------------
        guard_label = Label(name=f"L_unroll_{func.name}_{_fresh_suffix()}")
        adj = wrap32((UNROLL_FACTOR - 1) * step)
        gbound = wrap32(bound_c - adj)

        gtmp = _fresh_temp(func)
        new_block: List[TACInstruction] = [
            TACInstruction(Opcode.LABEL, dst=guard_label, annotation="unroll guard"),
            TACInstruction(rel, dst=gtmp,
                           src1=Var(name=iv, type_str="int"),
                           src2=Constant(gbound, "int")),
            TACInstruction(Opcode.JUMP_IF_FALSE, dst=Label(name=head_label), src1=gtmp),
        ]
        allocator = _TempAllocator(func)
        for _copy in range(UNROLL_FACTOR):
            new_block.extend(_rename_temps(body, allocator))
        new_block.append(TACInstruction(Opcode.JUMP, dst=guard_label))

        func.instructions = insts[:h] + new_block + insts[h:]
        done.add(head_label)
        done.add(guard_label.name)   # the prologue is itself a loop; leave it be
        return True

    return False


def _already_unrolled(insts: List[TACInstruction], head_label: str) -> bool:
    """True if `head_label` is already the remainder of an unroll prologue --
    i.e. some `L_unroll_*` guard block branches into it."""
    for k, ins in enumerate(insts):
        if (ins.opcode == Opcode.JUMP_IF_FALSE and str(ins.dst) == head_label
                and k >= 2 and insts[k - 2].opcode == Opcode.LABEL
                and str(insts[k - 2].dst).startswith("L_unroll_")):
            return True
    return False


def _match_iv_bound(cmp_i: TACInstruction) -> Tuple[Optional[str], Optional[int], Optional[Opcode]]:
    """Return (iv_name, bound_const, relation) if cmp is `iv REL const` / `const REL iv`."""
    n1, n2 = op_name(cmp_i.src1), op_name(cmp_i.src2)
    c1, c2 = const_int_value(cmp_i.src1), const_int_value(cmp_i.src2)
    if n1 and c2 is not None and c2 > 0:
        return n1, c2, cmp_i.opcode
    if n2 and c1 is not None and c1 > 0:
        # const REL iv  ->  iv INV_REL const
        flip = {Opcode.LT: Opcode.GT, Opcode.LE: Opcode.GE,
                Opcode.GT: Opcode.LT, Opcode.GE: Opcode.LE}
        return n2, c1, flip[cmp_i.opcode]
    return None, None, None


def _single_iv_step(body: List[TACInstruction], iv: str) -> Optional[int]:
    """`iv` must be updated exactly once, by `iv = iv +/- const` (direct or staged)."""
    defs = [b for b in body if defined_name(b) == iv]
    if len(defs) != 1:
        return None
    d = defs[0]
    if d.opcode == Opcode.ADD and op_name(d.src1) == iv:
        return const_int_value(d.src2)
    if d.opcode == Opcode.ADD and op_name(d.src2) == iv:
        return const_int_value(d.src1)
    if d.opcode == Opcode.SUB and op_name(d.src1) == iv:
        c = const_int_value(d.src2)
        return -c if c is not None else None
    if d.opcode == Opcode.ASSIGN and isinstance(d.src1, Temp):
        t = str(d.src1)
        tdefs = [b for b in body if defined_name(b) == t]
        if len(tdefs) == 1:
            return _staged(tdefs[0], iv)
    return None


def _staged(t_def: TACInstruction, iv: str) -> Optional[int]:
    if t_def.opcode == Opcode.ADD and op_name(t_def.src1) == iv:
        return const_int_value(t_def.src2)
    if t_def.opcode == Opcode.ADD and op_name(t_def.src2) == iv:
        return const_int_value(t_def.src1)
    if t_def.opcode == Opcode.SUB and op_name(t_def.src1) == iv:
        c = const_int_value(t_def.src2)
        return -c if c is not None else None
    return None


def _has_loop_carried_temp(body: List[TACInstruction]) -> bool:
    written: Set[str] = set()
    for b in body:
        for o in (b.src1, b.src2, b.src3):
            if isinstance(o, Temp) and str(o) not in written:
                return True   # read before written this iteration
        if isinstance(b.dst, Temp):
            written.add(str(b.dst))
    return False


def _writes_other_than_step(body: List[TACInstruction], iv: str) -> bool:
    seen_def = 0
    for b in body:
        if defined_name(b) == iv:
            seen_def += 1
        if b.opcode in (Opcode.STORE_ARR_1D, Opcode.STORE_ARR_2D, Opcode.SET_FIELD) \
                and op_name(b.dst) == iv:
            return True
    # the single ASSIGN-from-temp staged form counts the temp def too; allow 1-2
    return seen_def > 2


class _TempAllocator:
    """Hands out genuinely fresh temp ids and registers them in local_types."""

    def __init__(self, func: TACFunction):
        self.func = func
        mx = -1
        for ins in func.instructions:
            for o in (ins.dst, ins.src1, ins.src2, ins.src3):
                if isinstance(o, Temp) and o.id > mx:
                    mx = o.id
        for name in func.local_types:
            if name and name[0] == "t" and name[1:].isdigit():
                mx = max(mx, int(name[1:]))
        self.next_id = mx + 1

    def fresh(self, type_str: str = "int") -> Temp:
        t = Temp(id=self.next_id, type_str=type_str)
        self.next_id += 1
        self.func.local_types[str(t)] = type_str
        return t


def _fresh_temp(func: TACFunction, type_str: str = "int") -> Temp:
    return _TempAllocator(func).fresh(type_str)


def _rename_temps(body: List[TACInstruction], alloc: "_TempAllocator") -> List[TACInstruction]:
    """Deep-copy `body` with every temporary it *defines* remapped to a fresh id
    (uses of those temps are remapped too; temps defined outside stay put)."""
    local_defs: Set[str] = {str(b.dst) for b in body if isinstance(b.dst, Temp)}
    remap: Dict[str, Temp] = {
        name: alloc.fresh(alloc.func.local_types.get(name, "int"))
        for name in local_defs
    }

    def sub(o):
        if isinstance(o, Temp) and str(o) in remap:
            return remap[str(o)]
        return o

    return [
        TACInstruction(
            opcode=b.opcode,
            dst=sub(b.dst),
            src1=sub(b.src1), src2=sub(b.src2), src3=sub(b.src3),
            annotation=b.annotation,
        )
        for b in body
    ]
