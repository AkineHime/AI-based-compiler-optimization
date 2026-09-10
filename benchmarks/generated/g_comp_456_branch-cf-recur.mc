// generated: composite branch+cf+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 12 + 30 * 10;
        } else {
            acc = acc + i * 12 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 6;
        int q = 23;
        int r = 37;
        acc = acc + p * p + q * p * q + p * q + r * r * p + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(320);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(5200000);
    s = s + part2(20000);
    return ((s % 251) + 251) % 251;
}
