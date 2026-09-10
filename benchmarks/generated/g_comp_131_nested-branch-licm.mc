// generated: composite nested+branch+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 2 + i * 27;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 20 + 30 * 26;
        } else {
            acc = acc + i * 7 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 196 * 160 + 33 * 33 + 160 * 160;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(371428);
    s = s + part1(1600000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
