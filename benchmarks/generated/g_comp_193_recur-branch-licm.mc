// generated: composite recur+branch+licm
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(320);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 13 + 27 * 4;
        } else {
            acc = acc + i * 7 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 46 * 46 + 46 * 26 + 26 * 46 + 26 * 199;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(11538);
    s = s + part1(800000);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
