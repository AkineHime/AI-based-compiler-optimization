// generated: composite sr+cse+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 23 + i * 11 + i * 17 + 2;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 18) % 3571;
        int c1 = (x * 18) % 3571;
        int c2 = (x * 18) % 3571;
        int c3 = (x * 18) % 3571;
        int c4 = (x * 18) % 3571;
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
        int p = 20;
        int q = 4;
        int r = 29;
        acc = acc + q * p * q + q * r + p * p + p * q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(366666);
    return ((s % 251) + 251) % 251;
}
