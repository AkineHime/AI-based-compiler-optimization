// generated: composite licm+licm+unroll

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 185 * 113 * 93 + 113 * 113 + 185 * 185;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 149 * 149 + 55 * 28 * 149 + 149 * 55 * 28 + 28 * 28;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 4 - (i - (i / 8) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(800000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
