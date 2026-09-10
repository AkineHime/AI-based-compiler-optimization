// generated: composite licm+div+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 191 * 50 + 72 * 191 * 50 + 50 * 50 + 191 * 191;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 76370;
        int v = 69052;
        acc = acc + 1102988307 / u + 1895973201 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec2(320);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(400000);
    s = s + part2(6153);
    return ((s % 251) + 251) % 251;
}
