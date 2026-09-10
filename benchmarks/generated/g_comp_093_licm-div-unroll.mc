// generated: composite licm+div+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 166 * 101 + 76 * 101 * 166 + 101 * 101 + 101 * 166;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 52557;
        int v = 95817;
        acc = acc + 1628785038 / u + 1346000131 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 3 - (i - (i / 8) * 4);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3400000);
    s = s + part1(300000);
    s = s + part2(550000);
    return ((s % 251) + 251) % 251;
}
