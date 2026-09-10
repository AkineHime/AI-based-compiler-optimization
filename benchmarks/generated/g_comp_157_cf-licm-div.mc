// generated: composite cf+licm+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 40;
        int q = 15;
        int r = 7;
        acc = acc + p * q + r * r * p + p * q * r + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 53 * 14 * 184 + 14 * 184 + 184 * 53 + 53 * 53 + 184 * 184;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 95919;
        int v = 88654;
        acc = acc + 1156784117 / u + 1544379970 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(5200000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
