// generated: composite cf+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 18;
        int q = 21;
        int r = 37;
        acc = acc + q * r + p * p + q * p * q + (i - (i / 7) * 7);
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
        while (j < 24) {
            inner = inner + j * 22 + i * 4;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(76923);
    return ((s % 251) + 251) % 251;
}
