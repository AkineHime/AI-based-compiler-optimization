// generated: composite div+licm+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 97558;
        int v = 89436;
        acc = acc + 731004074 / u + 666750929 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 189 * 114 + 48 * 48 + 48 * 189;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 40;
        int q = 7;
        int r = 17;
        acc = acc + p * p + q * p * q + r * r * p + p * q * r + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
