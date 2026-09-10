// generated: composite sr+div+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 99743;
        int v = 59838;
        acc = acc + 423845929 / u + 1179388909 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec2(200);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(400000);
    s = s + part2(11538);
    return ((s % 251) + 251) % 251;
}
