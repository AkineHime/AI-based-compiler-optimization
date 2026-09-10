// generated: composite cf+recur+licm
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 39;
        int q = 11;
        int r = 30;
        acc = acc + p * q * r + p * p + p * q + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(200);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 168 * 168 + 59 * 39 * 168 + 39 * 168 + 168 * 59 + 39 * 39 + 168 * 59 * 39;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(6153);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
