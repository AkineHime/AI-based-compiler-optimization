// generated: composite recur+cf+nested+div
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(240);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 8;
        int q = 3;
        int r = 29;
        acc = acc + p * q + p * q * r + p * p + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 9 + i * 7;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 94501;
        int v = 64058;
        acc = acc + 178749981 / u + 451087977 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(300000);
    s = s + part2(130769);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
