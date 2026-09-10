// generated: composite licm+nested+sr

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 81 * 81 + 150 * 150 + 81 * 93 * 150 + 150 * 81 + 150 * 81 * 93;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 6 + i * 15;
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
        acc = acc + i * 17 + i * 3 + i * 57 + 8;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(114285);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
