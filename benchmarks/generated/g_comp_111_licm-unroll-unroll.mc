// generated: composite licm+unroll+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 156 * 39 + 39 * 85 * 156 + 156 * 156;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 4) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 2 - (i - (i / 9) * 4);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(600000);
    s = s + part1(1700000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
