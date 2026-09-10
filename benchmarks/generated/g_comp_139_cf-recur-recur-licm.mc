// generated: composite cf+recur+recur+licm
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 5;
}
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 28;
        int q = 18;
        int r = 17;
        acc = acc + q * r + p * q * r + q * p * q + r * r * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(460);
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

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 15 * 15 + 37 * 15 + 37 * 37;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(6153);
    s = s + part2(11538);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
