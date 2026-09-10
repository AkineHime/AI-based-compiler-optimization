// generated: composite cse+cf+branch+recur
int rec3(int n) {
    if (n < 2) { return n; }
    return rec3(n - 1) + 7;
}

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 42) % 10007;
        int c1 = (x * 42) % 10007;
        int c2 = (x * 42) % 10007;
        int c3 = (x * 42) % 10007;
        int c4 = (x * 42) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 29;
        int q = 7;
        int r = 31;
        acc = acc + q * p * q + p * q * r + q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 38 + 35 * 10;
        } else {
            acc = acc + i * 35 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec3(240);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(500000);
    s = s + part1(1133333);
    s = s + part2(666666);
    s = s + part3(4000);
    return ((s % 251) + 251) % 251;
}
