// generated: composite cf+licm+sr+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 30;
        int q = 10;
        int r = 8;
        acc = acc + r * r * p + q * p * q + q * r + p * q + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 184 * 184 + 101 * 35 + 101 * 184;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 13 + i * 57 + 5;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 12 + 34 * 39;
        } else {
            acc = acc + i * 24 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(300000);
    s = s + part2(1100000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
