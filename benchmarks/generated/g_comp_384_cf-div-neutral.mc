// generated: composite cf+div+neutral

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 19;
        int q = 3;
        int r = 29;
        acc = acc + p * q * r + p * q + r * r * p + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 76372;
        int v = 45047;
        acc = acc + 1740048761 / u + 1980324670 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(1300000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
