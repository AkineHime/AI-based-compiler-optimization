// generated: composite cse+div+cf+licm

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 80) % 7919;
        int c1 = (x * 80) % 7919;
        int c2 = (x * 80) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 94427;
        int v = 90257;
        acc = acc + 1526018609 / u + 928802481 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 26;
        int q = 29;
        int r = 21;
        acc = acc + p * p + p * q + q * r + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 50 * 50 + 50 * 116 + 63 * 63;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(750000);
    s = s + part2(1600000);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
