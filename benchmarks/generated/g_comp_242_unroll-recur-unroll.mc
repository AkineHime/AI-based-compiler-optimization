// generated: composite unroll+recur+unroll
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 3 - (i - (i / 4) * 6);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(100);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 - (i - (i / 8) * 9);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(4000);
    s = s + part2(1000000);
    return ((s % 251) + 251) % 251;
}
