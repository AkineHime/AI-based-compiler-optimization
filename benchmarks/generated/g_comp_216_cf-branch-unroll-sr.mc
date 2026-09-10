// generated: composite cf+branch+unroll+sr

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 8;
        int q = 18;
        int r = 32;
        acc = acc + p * q + q * p * q + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 28 + 9 * 15;
        } else {
            acc = acc + i * 29 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 6 - (i - (i / 5) * 5);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 17 + i * 11 + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(1133333);
    s = s + part2(300000);
    s = s + part3(2000000);
    return ((s % 251) + 251) % 251;
}
