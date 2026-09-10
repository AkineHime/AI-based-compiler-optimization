// generated: composite licm+nested+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 178 * 192 + 178 * 178 + 192 * 192 + 192 * 146 + 192 * 146 * 178 + 146 * 178 * 192;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 4 + i * 25;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 126 * 71 * 56 + 126 * 56 + 71 * 56 * 126 + 71 * 71 + 126 * 126;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(214285);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
