// generated: composite nested+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 9 + i * 16;
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
        acc = acc + rec1(460);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(214285);
    s = s + part1(11538);
    return ((s % 251) + 251) % 251;
}
