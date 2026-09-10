// generated: composite branch+cse+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 7 + 29 * 35;
        } else {
            acc = acc + i * 19 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 58) % 7919;
        int c1 = (x * 58) % 7919;
        int c2 = (x * 58) % 7919;
        int c3 = (x * 58) % 7919;
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
        int p = 12;
        int q = 34;
        int r = 11;
        acc = acc + r * r * p + q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
