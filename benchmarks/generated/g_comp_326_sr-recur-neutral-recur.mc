// generated: composite sr+recur+neutral+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 6;
}
int rec3(int n) {
    if (n < 2) { return n; }
    return rec3(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 3 + i * 11 + i * 57 + 4;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(200);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec3(200);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(6000);
    s = s + part2(3000000);
    s = s + part3(6000);
    return ((s % 251) + 251) % 251;
}
