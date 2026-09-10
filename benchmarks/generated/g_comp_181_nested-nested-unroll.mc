// generated: composite nested+nested+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 15 + i * 4;
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
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 28 + i * 18;
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
        acc = acc + i * 3 - (i - (i / 4) * 9);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(60000);
    s = s + part1(114285);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
