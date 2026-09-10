// generated: composite sr+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 7;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 23 + 1;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(60);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(2000000);
    s = s + part1(4000);
    return ((s % 251) + 251) % 251;
}
