// generated: composite div+neutral+recur+cse
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 59038;
        int v = 69242;
        acc = acc + 1592534827 / u + 340085291 / v + i / (u - (u / 100) * 100 + 1);
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
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec2(100);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 13) % 6997;
        int c1 = (x * 13) % 6997;
        int c2 = (x * 13) % 6997;
        int c3 = (x * 13) % 6997;
        int c4 = (x * 13) % 6997;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(666666);
    s = s + part2(4000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
