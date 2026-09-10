// generated: composite branch+cf+recur+div
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 30 + 8 * 21;
        } else {
            acc = acc + i * 9 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 20;
        int q = 33;
        int r = 13;
        acc = acc + p * q * r + r * r * p + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(240);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 73868;
        int v = 67885;
        acc = acc + 329935910 / u + 1866546882 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(1133333);
    s = s + part2(4000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
