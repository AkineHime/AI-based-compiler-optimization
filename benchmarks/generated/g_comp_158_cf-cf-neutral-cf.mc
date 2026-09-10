// generated: composite cf+cf+neutral+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 29;
        int q = 14;
        int r = 24;
        acc = acc + r * r * p + p * q + q * p * q + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 12;
        int q = 19;
        int r = 32;
        acc = acc + p * q * r + q * p * q + p * q + p * p + (i - (i / 7) * 7);
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

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 38;
        int q = 10;
        int r = 20;
        acc = acc + q * r + p * q + r * r * p + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(5200000);
    s = s + part2(5200000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
