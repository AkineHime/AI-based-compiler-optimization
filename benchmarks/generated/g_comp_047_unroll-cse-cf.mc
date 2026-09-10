// generated: composite unroll+cse+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 4 - (i - (i / 4) * 8);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 43) % 10007;
        int c1 = (x * 43) % 10007;
        int c2 = (x * 43) % 10007;
        int c3 = (x * 43) % 10007;
        int c4 = (x * 43) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 22;
        int q = 11;
        int r = 12;
        acc = acc + q * r + p * p + q * p * q + p * q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(300000);
    s = s + part2(1133333);
    return ((s % 251) + 251) % 251;
}
