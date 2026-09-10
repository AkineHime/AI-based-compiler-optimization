// generated: composite cf+recur+cse
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 7;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 22;
        int q = 8;
        int r = 17;
        acc = acc + p * p + p * q * r + p * q + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(240);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 64) % 4093;
        int c1 = (x * 64) % 4093;
        int c2 = (x * 64) % 4093;
        int c3 = (x * 64) % 4093;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(4000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
