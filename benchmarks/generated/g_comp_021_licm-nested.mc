// generated: composite licm+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 142 * 142 + 79 * 79 + 142 * 79 + 32 * 32 + 32 * 142 + 142 * 32;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 10 + i * 9;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(2000000);
    s = s + part1(40000);
    return ((s % 251) + 251) % 251;
}
