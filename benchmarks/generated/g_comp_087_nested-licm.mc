// generated: composite nested+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 14 + i * 24;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 94 * 186 * 176 + 186 * 186 + 176 * 176 + 94 * 186 + 94 * 176 + 94 * 94;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(130769);
    s = s + part1(2000000);
    return ((s % 251) + 251) % 251;
}
