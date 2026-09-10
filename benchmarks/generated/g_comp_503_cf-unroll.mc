// generated: composite cf+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 7;
        int q = 20;
        int r = 17;
        acc = acc + p * p + r * r * p + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 6) * 9);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
