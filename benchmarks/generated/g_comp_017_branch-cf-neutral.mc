// generated: composite branch+cf+neutral

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 9 + 14 * 5;
        } else {
            acc = acc + i * 20 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 10;
        int q = 28;
        int r = 11;
        acc = acc + p * p + q * p * q + p * q + q * r + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(1133333);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
