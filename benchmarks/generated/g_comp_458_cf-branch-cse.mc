// generated: composite cf+branch+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 21;
        int q = 16;
        int r = 40;
        acc = acc + q * p * q + r * r * p + p * p + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 4 + 7 * 18;
        } else {
            acc = acc + i * 24 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 42) % 6997;
        int c1 = (x * 42) % 6997;
        int c2 = (x * 42) % 6997;
        int c3 = (x * 42) % 6997;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(300000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
