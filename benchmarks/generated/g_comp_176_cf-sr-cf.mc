// generated: composite cf+sr+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 19;
        int q = 35;
        int r = 33;
        acc = acc + p * p + q * p * q + r * r * p + q * r + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 17 + i * 57 + i * 5 + 6;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 39;
        int q = 25;
        int r = 3;
        acc = acc + p * p + q * r + r * r * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(800000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
