// generated: composite licm+licm+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 183 * 183 + 154 * 154 + 183 * 110 + 183 * 154 * 110 + 154 * 110 * 183;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 21 * 21 + 21 * 35 * 130 + 130 * 130 + 21 * 35 + 35 * 35;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 17 + 20 * 26;
        } else {
            acc = acc + i * 10 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(800000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
