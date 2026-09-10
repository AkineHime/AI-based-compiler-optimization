// generated: composite cf+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 35;
        int q = 33;
        int r = 23;
        acc = acc + q * r + q * p * q + p * p + p * q * r + (i - (i / 7) * 7);
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

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(4000);
    return ((s % 251) + 251) % 251;
}
