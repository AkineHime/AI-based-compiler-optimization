// generated: composite recur+licm+recur+neutral
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 4;
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
        acc = acc + 41 * 153 * 185 + 185 * 185 + 153 * 153 + 153 * 185 + 41 * 41 + 185 * 41;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(200);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6000);
    s = s + part1(1600000);
    s = s + part2(6000);
    s = s + part3(1600000);
    return ((s % 251) + 251) % 251;
}
