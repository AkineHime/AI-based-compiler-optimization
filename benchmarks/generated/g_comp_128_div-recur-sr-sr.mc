// generated: composite div+recur+sr+sr
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 95684;
        int v = 89421;
        acc = acc + 612624749 / u + 1174967617 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(120);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 + i * 23 + 5;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 57 + i * 13 + i * 31 + 4;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(11538);
    s = s + part2(400000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
