// generated: composite nested+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 7 + i * 11;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 25;
        int q = 7;
        int r = 31;
        acc = acc + p * p + q * r + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(114285);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
