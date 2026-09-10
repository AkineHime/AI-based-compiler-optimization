// generated: composite nested+unroll+cse+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 9 + i * 18;
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
        acc = acc + i * 7 - (i - (i / 4) * 3);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 46) % 10007;
        int c1 = (x * 46) % 10007;
        int c2 = (x * 46) % 10007;
        int c3 = (x * 46) % 10007;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 198 * 44 * 30 + 198 * 44 + 30 * 198 + 198 * 198 + 30 * 30 + 198 * 30;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(60000);
    s = s + part1(400000);
    s = s + part2(1000000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
