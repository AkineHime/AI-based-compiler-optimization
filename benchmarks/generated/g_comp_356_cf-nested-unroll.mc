// generated: composite cf+nested+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 38;
        int q = 37;
        int r = 13;
        acc = acc + p * q + p * p + r * r * p + p * q * r + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 11 + i * 26;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 4) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(40000);
    s = s + part2(1000000);
    return ((s % 251) + 251) % 251;
}
