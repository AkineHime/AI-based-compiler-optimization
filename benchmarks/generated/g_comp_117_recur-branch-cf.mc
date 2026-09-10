// generated: composite recur+branch+cf
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(60);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 14 + 27 * 20;
        } else {
            acc = acc + i * 24 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 22;
        int q = 34;
        int r = 23;
        acc = acc + p * q + r * r * p + p * q * r + q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(366666);
    s = s + part2(1133333);
    return ((s % 251) + 251) % 251;
}
