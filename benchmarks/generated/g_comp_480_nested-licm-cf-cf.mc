// generated: composite nested+licm+cf+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 4 + i * 29;
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
        acc = acc + 153 * 164 + 164 * 40 * 153 + 153 * 153 + 40 * 153;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 37;
        int q = 23;
        int r = 32;
        acc = acc + q * p * q + q * r + p * q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 6;
        int q = 3;
        int r = 12;
        acc = acc + p * q * r + q * p * q + p * p + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(40000);
    s = s + part1(2000000);
    s = s + part2(666666);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
