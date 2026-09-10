// generated: composite cf+branch+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 11;
        int q = 11;
        int r = 8;
        acc = acc + p * q + p * q * r + q * r + r * r * p + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 22 + 30 * 17;
        } else {
            acc = acc + i * 36 - (i - (i / 5) * 5);
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
        int c0 = (x * 77) % 4093;
        int c1 = (x * 77) % 4093;
        int c2 = (x * 77) % 4093;
        int c3 = (x * 77) % 4093;
        int c4 = (x * 77) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1600000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
