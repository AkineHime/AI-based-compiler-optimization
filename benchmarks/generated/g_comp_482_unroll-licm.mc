// generated: composite unroll+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 2 - (i - (i / 5) * 4);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 46 * 54 * 90 + 54 * 90 * 46 + 90 * 46 + 46 * 54;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1700000);
    s = s + part1(2000000);
    return ((s % 251) + 251) % 251;
}
