// generated: composite recur+recur
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 3;
}
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(200);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(120);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6000);
    s = s + part1(20000);
    return ((s % 251) + 251) % 251;
}
