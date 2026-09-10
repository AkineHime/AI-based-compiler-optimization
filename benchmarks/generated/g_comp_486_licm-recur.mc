// generated: composite licm+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 177 * 177 + 177 * 20 + 176 * 177 * 20 + 20 * 176;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(60);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(4000);
    return ((s % 251) + 251) % 251;
}
