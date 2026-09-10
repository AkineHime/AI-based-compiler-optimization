// generated: composite recur+div+sr
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(120);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 44377;
        int v = 72907;
        acc = acc + 106674000 / u + 1929515450 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 11 + i * 23 + i * 57 + 4;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(11538);
    s = s + part1(1300000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
