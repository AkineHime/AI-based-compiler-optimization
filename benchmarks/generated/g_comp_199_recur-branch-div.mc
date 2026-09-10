// generated: composite recur+branch+div
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(100);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 37 + 34 * 20;
        } else {
            acc = acc + i * 8 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 49770;
        int v = 68055;
        acc = acc + 1734345330 / u + 277415608 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(300000);
    s = s + part2(680000);
    return ((s % 251) + 251) % 251;
}
