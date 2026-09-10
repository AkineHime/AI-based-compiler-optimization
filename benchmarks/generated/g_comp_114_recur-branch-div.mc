// generated: composite recur+branch+div
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 5;
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
            acc = acc + i * 19 + 17 * 18;
        } else {
            acc = acc + i * 15 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 76805;
        int v = 55508;
        acc = acc + 1984544536 / u + 1157894852 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6000);
    s = s + part1(3000000);
    s = s + part2(1300000);
    return ((s % 251) + 251) % 251;
}
