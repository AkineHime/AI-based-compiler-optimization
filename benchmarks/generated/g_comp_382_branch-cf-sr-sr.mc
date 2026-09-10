// generated: composite branch+cf+sr+sr

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 26 + 27 * 7;
        } else {
            acc = acc + i * 20 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 34;
        int q = 12;
        int r = 23;
        acc = acc + p * p + r * r * p + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 31 + i * 11 + 9;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 + 8;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(5200000);
    s = s + part2(5200000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
