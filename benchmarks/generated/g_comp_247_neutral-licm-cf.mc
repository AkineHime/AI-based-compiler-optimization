// generated: composite neutral+licm+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 110 * 110 + 91 * 91 + 110 * 116 * 91 + 91 * 110 + 91 * 110 * 116 + 91 * 116;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 29;
        int q = 29;
        int r = 16;
        acc = acc + q * r + p * q + p * p + p * q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(2000000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
