// generated: composite cse+branch+recur+nested
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 13) % 3571;
        int c1 = (x * 13) % 3571;
        int c2 = (x * 13) % 3571;
        int c3 = (x * 13) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 30 + 16 * 25;
        } else {
            acc = acc + i * 32 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec2(320);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 3 + i * 11;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(533333);
    s = s + part1(400000);
    s = s + part2(11538);
    s = s + part3(371428);
    return ((s % 251) + 251) % 251;
}
