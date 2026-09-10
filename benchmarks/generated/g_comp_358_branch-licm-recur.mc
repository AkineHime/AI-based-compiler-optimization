// generated: composite branch+licm+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 37 + 22 * 22;
        } else {
            acc = acc + i * 9 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 29 * 54 * 30 + 30 * 30 + 29 * 29 + 54 * 54 + 30 * 54 + 30 * 29 * 54;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(100);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(1100000);
    s = s + part2(4000);
    return ((s % 251) + 251) % 251;
}
