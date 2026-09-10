// generated: composite recur+unroll
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(460);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 2 - (i - (i / 4) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(11538);
    s = s + part1(3000000);
    return ((s % 251) + 251) % 251;
}
