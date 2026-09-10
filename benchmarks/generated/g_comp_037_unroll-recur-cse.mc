// generated: composite unroll+recur+cse
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 8 - (i - (i / 9) * 5);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(460);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 49) % 10007;
        int c1 = (x * 49) % 10007;
        int c2 = (x * 49) % 10007;
        int c3 = (x * 49) % 10007;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(6000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
