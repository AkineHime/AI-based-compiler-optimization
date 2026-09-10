// generated: composite branch+licm+unroll+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 24 + 28 * 18;
        } else {
            acc = acc + i * 24 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 155 * 93 * 113 + 113 * 113 + 113 * 155;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 9) * 6);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 146 * 104 + 104 * 104 + 38 * 38 + 38 * 146 * 104;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(1100000);
    s = s + part2(300000);
    s = s + part3(3400000);
    return ((s % 251) + 251) % 251;
}
