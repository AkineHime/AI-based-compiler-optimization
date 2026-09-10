// generated: composite recur+licm
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(160);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 46 * 46 + 124 * 11 * 46 + 124 * 124 + 46 * 124 + 46 * 124 * 11;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(600000);
    return ((s % 251) + 251) % 251;
}
