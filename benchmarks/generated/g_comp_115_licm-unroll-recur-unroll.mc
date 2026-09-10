// generated: composite licm+unroll+recur+unroll
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 108 * 185 + 98 * 108 * 185 + 185 * 98 * 108 + 185 * 185 + 98 * 98 + 185 * 108;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 6 - (i - (i / 6) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(460);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 8 - (i - (i / 7) * 5);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(11538);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
