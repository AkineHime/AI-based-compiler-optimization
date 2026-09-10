// generated: composite licm+cf+sr+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 127 * 173 + 127 * 22 + 127 * 173 * 22;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 9;
        int q = 19;
        int r = 10;
        acc = acc + p * p + p * q + p * q * r + q * p * q + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 11 + i * 3 + 5;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 6 - (i - (i / 5) * 8);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3400000);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
