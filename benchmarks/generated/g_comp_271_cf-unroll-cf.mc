// generated: composite cf+unroll+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 9;
        int q = 18;
        int r = 31;
        acc = acc + p * p + p * q + p * q * r + q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 7 - (i - (i / 4) * 9);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 36;
        int q = 20;
        int r = 34;
        acc = acc + p * q * r + p * q + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(1000000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
