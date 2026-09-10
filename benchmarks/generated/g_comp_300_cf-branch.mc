// generated: composite cf+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 24;
        int q = 12;
        int r = 9;
        acc = acc + r * r * p + q * p * q + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 23 + 26 * 8;
        } else {
            acc = acc + i * 29 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(5200000);
    return ((s % 251) + 251) % 251;
}
