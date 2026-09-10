// generated: composite cf+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 14;
        int q = 16;
        int r = 22;
        acc = acc + r * r * p + p * q + q * p * q + p * q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 51 * 26 * 44 + 44 * 26 + 44 * 44 + 44 * 51 * 26;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(2000000);
    return ((s % 251) + 251) % 251;
}
