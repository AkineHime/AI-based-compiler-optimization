// generated: composite branch+sr+sr

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 19 + 26 * 26;
        } else {
            acc = acc + i * 13 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 + 5;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 11 + 4;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(3000000);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
