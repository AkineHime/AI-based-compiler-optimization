// generated: composite licm+nested+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 22 * 51 * 161 + 22 * 51 + 51 * 51 + 22 * 22;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 30 + i * 17;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 28;
        int q = 34;
        int r = 4;
        acc = acc + p * q + q * r + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(60000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
