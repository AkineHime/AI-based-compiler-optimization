// generated: composite recur+cse+neutral
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 7;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(60);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 73) % 3571;
        int c1 = (x * 73) % 3571;
        int c2 = (x * 73) % 3571;
        int c3 = (x * 73) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
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

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(300000);
    s = s + part2(1133333);
    return ((s % 251) + 251) % 251;
}
