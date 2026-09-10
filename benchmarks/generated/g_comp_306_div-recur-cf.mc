// generated: composite div+recur+cf
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 84651;
        int v = 79015;
        acc = acc + 1095919764 / u + 1765502013 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(120);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 31;
        int q = 9;
        int r = 10;
        acc = acc + q * p * q + p * q * r + p * q + q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(750000);
    s = s + part1(6153);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
