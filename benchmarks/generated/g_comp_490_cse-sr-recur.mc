// generated: composite cse+sr+recur
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 83) % 6997;
        int c1 = (x * 83) % 6997;
        int c2 = (x * 83) % 6997;
        int c3 = (x * 83) % 6997;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 17 + 1;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(60);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(850000);
    s = s + part1(600000);
    s = s + part2(4000);
    return ((s % 251) + 251) % 251;
}
