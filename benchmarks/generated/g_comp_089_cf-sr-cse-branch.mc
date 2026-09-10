// generated: composite cf+sr+cse+branch

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 14;
        int q = 12;
        int r = 32;
        acc = acc + q * r + p * q + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 23 + i * 17 + 7;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 32) % 10007;
        int c1 = (x * 32) % 10007;
        int c2 = (x * 32) % 10007;
        int c3 = (x * 32) % 10007;
        int c4 = (x * 32) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 27 + 9 * 26;
        } else {
            acc = acc + i * 25 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(1133333);
    return ((s % 251) + 251) % 251;
}
