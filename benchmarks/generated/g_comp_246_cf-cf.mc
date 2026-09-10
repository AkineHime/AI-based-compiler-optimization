// generated: composite cf+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 19;
        int q = 3;
        int r = 22;
        acc = acc + p * q * r + r * r * p + p * p + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 3;
        int q = 10;
        int r = 24;
        acc = acc + r * r * p + q * p * q + p * q + p * q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
