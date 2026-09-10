// generated: composite branch+branch+nested+branch

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 6 + 20 * 40;
        } else {
            acc = acc + i * 3 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 29 + 39 * 6;
        } else {
            acc = acc + i * 11 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 24) {
            inner = inner + j * 4 + i * 15;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 38 + 36 * 26;
        } else {
            acc = acc + i * 36 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(3000000);
    s = s + part2(60000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
