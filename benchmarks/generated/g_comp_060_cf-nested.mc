// generated: composite cf+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 28;
        int q = 18;
        int r = 6;
        acc = acc + r * r * p + q * p * q + p * q * r + q * r + (i - (i / 7) * 7);
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
        while (j < 6) {
            inner = inner + j * 24 + i * 21;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(60000);
    return ((s % 251) + 251) % 251;
}
