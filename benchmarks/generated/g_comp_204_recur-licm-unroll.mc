// generated: composite recur+licm+unroll
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(460);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 61 * 77 * 52 + 77 * 77 + 52 * 61;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 9 - (i - (i / 6) * 6);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(20000);
    s = s + part1(800000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
