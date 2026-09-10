// generated: composite cf+unroll+branch

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 38;
        int q = 26;
        int r = 7;
        acc = acc + r * r * p + p * p + p * q * r + p * q + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 7) * 5);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 25 + 29 * 4;
        } else {
            acc = acc + i * 21 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(400000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
