// generated: composite cf+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 5;
        int q = 8;
        int r = 21;
        acc = acc + p * q * r + q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 9;
        int q = 3;
        int r = 37;
        acc = acc + p * q * r + q * r + r * r * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
