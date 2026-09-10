// generated: composite recur+neutral+cse
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(60);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 90) % 3571;
        int c1 = (x * 90) % 3571;
        int c2 = (x * 90) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(366666);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
