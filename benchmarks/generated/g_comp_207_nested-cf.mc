// generated: composite nested+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 24 + i * 20;
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
        int p = 16;
        int q = 35;
        int r = 35;
        acc = acc + q * p * q + r * r * p + q * r + p * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(60000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
