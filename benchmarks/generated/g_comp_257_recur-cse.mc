// generated: composite recur+cse
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 7;
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
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 95) % 10007;
        int c1 = (x * 95) % 10007;
        int c2 = (x * 95) % 10007;
        int c3 = (x * 95) % 10007;
        int c4 = (x * 95) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(850000);
    return ((s % 251) + 251) % 251;
}
