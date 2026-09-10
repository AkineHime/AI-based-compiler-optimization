// generated: composite licm+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 94 * 185 + 27 * 94 * 185 + 27 * 27 + 185 * 94 + 185 * 185;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 2 - (i - (i / 7) * 3);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3400000);
    s = s + part1(1000000);
    return ((s % 251) + 251) % 251;
}
