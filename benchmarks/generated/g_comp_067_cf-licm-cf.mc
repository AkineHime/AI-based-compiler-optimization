// generated: composite cf+licm+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 20;
        int q = 27;
        int r = 20;
        acc = acc + p * q * r + q * p * q + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 78 * 102 + 156 * 156 + 102 * 156 * 78 + 156 * 78;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 18;
        int q = 12;
        int r = 7;
        acc = acc + p * q * r + q * r + p * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(3000000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
