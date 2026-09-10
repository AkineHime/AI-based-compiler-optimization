// generated: composite recur+unroll
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(460);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 8) * 6);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
