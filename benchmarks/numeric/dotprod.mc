// Repeated dot product; the scale and offset terms are loop-invariant.
int main() {
    int x[400];
    int y[400];
    int i = 0;
    while (i < 400) {
        x[i] = (i * 5 + 2) - ((i * 5 + 2) / 19) * 19;
        y[i] = (i * 7 + 3) - ((i * 7 + 3) / 23) * 23;
        i = i + 1;
    }
    int s = 11;
    int o = 4;
    int acc = 0;
    int rep = 0;
    while (rep < 70000) {
        int d = 0;
        i = 0;
        while (i < 400) {
            d = d + x[i] * y[i] * s + o * s + s * s;
            i = i + 1;
        }
        acc = acc + d;
        rep = rep + 1;
    }
    return ((acc % 251) + 251) % 251;
}
