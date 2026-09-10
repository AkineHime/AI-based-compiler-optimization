// generated: composite cse+recur+cf
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 80) % 3571;
        int c1 = (x * 80) % 3571;
        int c2 = (x * 80) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(320);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 22;
        int q = 40;
        int r = 37;
        acc = acc + r * r * p + q * r + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(533333);
    s = s + part1(6000);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
