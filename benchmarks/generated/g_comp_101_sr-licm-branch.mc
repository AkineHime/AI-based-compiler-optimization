// generated: composite sr+licm+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 31 + 4;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 147 * 147 + 51 * 51 + 65 * 147 + 147 * 51 * 65;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 15 + 8 * 6;
        } else {
            acc = acc + i * 29 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(400000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
