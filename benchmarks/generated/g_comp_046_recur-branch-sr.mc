// generated: composite recur+branch+sr
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(120);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 19 + 14 * 37;
        } else {
            acc = acc + i * 13 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 13 + i * 11 + i * 3 + 3;
        i = i + 1;
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
