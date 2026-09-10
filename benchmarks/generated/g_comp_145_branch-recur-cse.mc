// generated: composite branch+recur+cse
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 16 + 21 * 3;
        } else {
            acc = acc + i * 19 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(460);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 49) % 6997;
        int c1 = (x * 49) % 6997;
        int c2 = (x * 49) % 6997;
        int c3 = (x * 49) % 6997;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(20000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
