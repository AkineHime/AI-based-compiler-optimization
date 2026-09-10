// generated: composite recur+cf+nested
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(460);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 15;
        int q = 20;
        int r = 16;
        acc = acc + p * q + q * r + q * p * q + p * p + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 20 + i * 24;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6153);
    s = s + part1(5200000);
    s = s + part2(114285);
    return ((s % 251) + 251) % 251;
}
