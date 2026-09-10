// generated: composite cf+licm+nested

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 21;
        int q = 16;
        int r = 6;
        acc = acc + q * r + p * p + r * r * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 42 * 162 * 19 + 162 * 162 + 162 * 19;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 30 + i * 19;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(2000000);
    s = s + part2(76923);
    return ((s % 251) + 251) % 251;
}
