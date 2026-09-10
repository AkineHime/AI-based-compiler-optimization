// generated: composite recur+unroll+licm+cse
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 3;
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
        acc = acc + i * 2 - (i - (i / 9) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 143 * 27 * 157 + 27 * 157 * 143 + 27 * 27 + 143 * 27;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 92) % 10007;
        int c1 = (x * 92) % 10007;
        int c2 = (x * 92) % 10007;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(550000);
    s = s + part2(2000000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
