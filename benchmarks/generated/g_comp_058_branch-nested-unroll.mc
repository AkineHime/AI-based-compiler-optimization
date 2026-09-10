// generated: composite branch+nested+unroll

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 18 + 39 * 31;
        } else {
            acc = acc + i * 28 - (i - (i / 5) * 5);
        }
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
            inner = inner + j * 7 + i * 30;
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
    s = s + part0(300000);
    s = s + part1(40000);
    s = s + part2(550000);
    return ((s % 251) + 251) % 251;
}
