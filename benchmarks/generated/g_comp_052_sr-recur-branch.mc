// generated: composite sr+recur+branch
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 7 + i * 5 + i * 23 + 5;
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
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 25 + 23 * 17;
        } else {
            acc = acc + i * 26 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(6000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
