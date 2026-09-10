// generated: composite licm+licm+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 193 * 193 * 139 + 193 * 139 + 193 * 193 + 139 * 193;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 50 * 123 + 123 * 50 + 123 * 123;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 35;
        int q = 32;
        int r = 6;
        acc = acc + q * p * q + p * q + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(1600000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
