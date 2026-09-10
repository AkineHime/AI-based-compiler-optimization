// generated: composite recur+licm
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(320);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 45 * 47 * 121 + 47 * 47 + 47 * 121 * 45 + 45 * 47;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(11538);
    s = s + part1(3000000);
    return ((s % 251) + 251) % 251;
}
