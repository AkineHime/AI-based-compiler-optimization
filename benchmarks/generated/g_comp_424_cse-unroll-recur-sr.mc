// generated: composite cse+unroll+recur+sr
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 75) % 4093;
        int c1 = (x * 75) % 4093;
        int c2 = (x * 75) % 4093;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 9 - (i - (i / 4) * 6);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(120);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 57 + i * 11 + i * 13 + 8;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(5200000);
    s = s + part2(6153);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
