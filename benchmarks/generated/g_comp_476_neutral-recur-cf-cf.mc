// generated: composite neutral+recur+cf+cf
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
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
        int p = 15;
        int q = 32;
        int r = 34;
        acc = acc + p * q + p * q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 40;
        int q = 6;
        int r = 15;
        acc = acc + p * q + q * p * q + p * q * r + q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(20000);
    s = s + part2(3000000);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
