// generated: composite div+cse+cse+recur
int rec3(int n) {
    if (n < 2) { return n; }
    return rec3(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 65364;
        int v = 68658;
        acc = acc + 1138367729 / u + 243259019 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 41) % 3571;
        int c1 = (x * 41) % 3571;
        int c2 = (x * 41) % 3571;
        int c3 = (x * 41) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 66) % 10007;
        int c1 = (x * 66) % 10007;
        int c2 = (x * 66) % 10007;
        int c3 = (x * 66) % 10007;
        int c4 = (x * 66) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec3(240);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(4000);
    return ((s % 251) + 251) % 251;
}
