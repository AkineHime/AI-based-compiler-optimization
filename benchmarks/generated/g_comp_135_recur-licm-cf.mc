// generated: composite recur+licm+cf
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 7;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(460);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 52 * 122 + 122 * 45 * 52 + 45 * 52 + 45 * 45;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 5;
        int q = 16;
        int r = 39;
        acc = acc + q * r + p * p + q * p * q + r * r * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(11538);
    s = s + part1(5200000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
