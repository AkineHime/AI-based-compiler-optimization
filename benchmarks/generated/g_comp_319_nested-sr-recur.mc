// generated: composite nested+sr+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 9 + i * 22;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 57 + i * 13 + i * 5 + 2;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(120);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(60000);
    s = s + part1(5200000);
    s = s + part2(6000);
    return ((s % 251) + 251) % 251;
}
