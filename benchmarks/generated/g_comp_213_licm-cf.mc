// generated: composite licm+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 12 * 12 + 71 * 72 + 71 * 12 + 12 * 72 * 71 + 72 * 72;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 31;
        int q = 35;
        int r = 18;
        acc = acc + p * p + q * p * q + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(2000000);
    s = s + part1(1133333);
    return ((s % 251) + 251) % 251;
}
