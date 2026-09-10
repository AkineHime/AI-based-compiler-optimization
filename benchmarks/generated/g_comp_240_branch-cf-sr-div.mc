// generated: composite branch+cf+sr+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 17 + 9 * 16;
        } else {
            acc = acc + i * 31 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 28;
        int q = 16;
        int r = 13;
        acc = acc + q * p * q + p * p + p * q + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 23 + i * 7 + i * 13 + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 52095;
        int v = 70922;
        acc = acc + 1188363405 / u + 550149089 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(3000000);
    s = s + part2(3000000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
