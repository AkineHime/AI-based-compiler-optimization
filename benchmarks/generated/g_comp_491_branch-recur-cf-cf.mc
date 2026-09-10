// generated: composite branch+recur+cf+cf
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 4;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 36 + 38 * 28;
        } else {
            acc = acc + i * 14 - (i - (i / 5) * 5);
        }
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
        int p = 3;
        int q = 9;
        int r = 32;
        acc = acc + r * r * p + p * p + q * r + q * p * q + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 8;
        int q = 28;
        int r = 23;
        acc = acc + q * r + p * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(6153);
    s = s + part2(1600000);
    s = s + part3(1600000);
    return ((s % 251) + 251) % 251;
}
