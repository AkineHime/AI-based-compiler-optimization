// generated: composite branch+cf+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 17 + 28 * 5;
        } else {
            acc = acc + i * 23 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 15;
        int q = 32;
        int r = 12;
        acc = acc + p * q * r + p * q + r * r * p + p * p + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 17 + i * 23 + 2;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(800000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
