// generated: composite unroll+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 - (i - (i / 8) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 103 * 103 + 103 * 77 + 103 * 114 * 77 + 114 * 114;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(600000);
    return ((s % 251) + 251) % 251;
}
