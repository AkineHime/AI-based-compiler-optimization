// generated: composite cf+div+cf+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 16;
        int q = 29;
        int r = 3;
        acc = acc + q * p * q + p * p + p * q * r + r * r * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 57287;
        int v = 76552;
        acc = acc + 863175333 / u + 1447709049 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 5;
        int q = 14;
        int r = 25;
        acc = acc + p * q * r + p * q + p * p + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 32 + 9 * 24;
        } else {
            acc = acc + i * 9 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(366666);
    return ((s % 251) + 251) % 251;
}
