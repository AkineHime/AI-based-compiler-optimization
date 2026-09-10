// generated: composite div+cf+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 77150;
        int v = 92611;
        acc = acc + 1449073131 / u + 1860365991 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 13;
        int q = 22;
        int r = 40;
        acc = acc + q * p * q + q * r + r * r * p + p * q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 47 * 47 + 187 * 187 + 47 * 187 * 69 + 47 * 69;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(750000);
    s = s + part1(400000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
