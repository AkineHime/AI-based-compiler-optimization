// generated: composite nested+branch+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 11 + i * 4;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 35 + 10 * 32;
        } else {
            acc = acc + i * 18 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 27;
        int q = 30;
        int r = 22;
        acc = acc + p * q * r + q * r + q * p * q + p * p + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(130769);
    s = s + part1(366666);
    s = s + part2(366666);
    return ((s % 251) + 251) % 251;
}
