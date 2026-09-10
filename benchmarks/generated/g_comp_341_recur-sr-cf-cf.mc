// generated: composite recur+sr+cf+cf
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(120);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 + i * 31 + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 40;
        int q = 5;
        int r = 36;
        acc = acc + q * r + r * r * p + p * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 29;
        int q = 23;
        int r = 16;
        acc = acc + q * r + p * q * r + q * p * q + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6000);
    s = s + part1(3000000);
    s = s + part2(800000);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
