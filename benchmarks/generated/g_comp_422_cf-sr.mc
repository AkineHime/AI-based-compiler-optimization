// generated: composite cf+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 34;
        int q = 7;
        int r = 18;
        acc = acc + q * p * q + p * q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 13 + 8;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(3400000);
    return ((s % 251) + 251) % 251;
}
