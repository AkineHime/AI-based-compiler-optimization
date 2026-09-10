// generated: composite sr+recur+sr
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 + i * 23 + i * 11 + 6;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(460);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 7 + i * 57 + 9;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(6153);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
