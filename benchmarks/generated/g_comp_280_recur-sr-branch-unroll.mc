// generated: composite recur+sr+branch+unroll
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(460);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 23 + i * 5 + 9;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 28 + 12 * 22;
        } else {
            acc = acc + i * 29 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 6 - (i - (i / 5) * 6);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(11538);
    s = s + part1(400000);
    s = s + part2(800000);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
