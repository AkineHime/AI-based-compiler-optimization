// generated: composite nested+cf+recur+licm
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 26 + i * 6;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 22;
        int q = 11;
        int r = 18;
        acc = acc + p * q + p * q * r + p * p + q * p * q + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(120);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 92 * 46 * 55 + 55 * 55 + 92 * 92;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(114285);
    s = s + part1(1600000);
    s = s + part2(6153);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
