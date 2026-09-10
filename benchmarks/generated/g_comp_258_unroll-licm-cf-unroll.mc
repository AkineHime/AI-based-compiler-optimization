// generated: composite unroll+licm+cf+unroll

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 4) * 5);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 177 * 114 + 114 * 177 + 84 * 84 + 84 * 114 * 177 + 177 * 177 + 177 * 84 * 114;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 38;
        int q = 14;
        int r = 26;
        acc = acc + p * q * r + r * r * p + q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 9 - (i - (i / 5) * 5);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1700000);
    s = s + part1(2000000);
    s = s + part2(666666);
    s = s + part3(1700000);
    return ((s % 251) + 251) % 251;
}
