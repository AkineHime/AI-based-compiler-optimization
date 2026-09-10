// generated: composite sr+branch+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 + 9;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 33 + 24 * 9;
        } else {
            acc = acc + i * 36 - (i - (i / 5) * 5);
        }
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
    s = s + part1(800000);
    s = s + part2(6153);
    return ((s % 251) + 251) % 251;
}
