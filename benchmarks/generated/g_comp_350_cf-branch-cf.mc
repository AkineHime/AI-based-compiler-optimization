// generated: composite cf+branch+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 37;
        int q = 11;
        int r = 7;
        acc = acc + p * p + p * q + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 11 + 4 * 13;
        } else {
            acc = acc + i * 34 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 33;
        int q = 3;
        int r = 19;
        acc = acc + p * q * r + p * q + p * p + q * p * q + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
