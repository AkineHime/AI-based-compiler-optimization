// generated: composite cf+cf+unroll+branch

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 10;
        int q = 8;
        int r = 17;
        acc = acc + p * q + p * q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 39;
        int q = 32;
        int r = 6;
        acc = acc + p * p + q * r + r * r * p + p * q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 - (i - (i / 6) * 9);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 38 + 29 * 40;
        } else {
            acc = acc + i * 11 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(800000);
    s = s + part2(400000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
