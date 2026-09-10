// generated: composite sr+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 13 + 9;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 7;
        int q = 30;
        int r = 10;
        acc = acc + p * p + p * q + q * r + r * r * p + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
