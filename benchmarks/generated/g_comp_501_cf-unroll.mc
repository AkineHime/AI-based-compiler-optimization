// generated: composite cf+unroll

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 16;
        int q = 19;
        int r = 32;
        acc = acc + p * q * r + r * r * p + q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 7) * 8);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
