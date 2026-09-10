// generated: composite licm+unroll+cse+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 75 * 191 * 102 + 102 * 102 + 102 * 75 * 191;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 6 - (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 85) % 7919;
        int c1 = (x * 85) % 7919;
        int c2 = (x * 85) % 7919;
        int c3 = (x * 85) % 7919;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 28;
        int q = 3;
        int r = 27;
        acc = acc + q * p * q + q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(3000000);
    s = s + part2(400000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
