// generated: composite cf+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 9;
        int q = 31;
        int r = 40;
        acc = acc + p * q + p * q * r + q * p * q + q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 28 + i * 3;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(42307);
    return ((s % 251) + 251) % 251;
}
