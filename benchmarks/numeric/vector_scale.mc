// Repeated scaled reduction; bias*scale and scale*scale are loop-invariant.
int main() {
    int v[256];
    int i = 0;
    while (i < 256) { v[i] = (i * 3 + 1) - ((i * 3 + 1) / 17) * 17; i = i + 1; }
    int scale = 5;
    int bias = 3;
    int acc = 0;
    int rep = 0;
    while (rep < 120000) {
        int s = 0;
        i = 0;
        while (i < 256) {
            s = s + v[i] * scale + bias * scale + scale * scale + bias * bias;
            i = i + 1;
        }
        acc = acc + s;
        rep = rep + 1;
    }
    return ((acc % 251) + 251) % 251;
}
