// generated: composite div+nested+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 40286;
        int v = 45719;
        acc = acc + 1364797169 / u + 1768768728 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 14 + i * 10;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 30 + 31 * 19;
        } else {
            acc = acc + i * 8 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(40000);
    s = s + part2(666666);
    return ((s % 251) + 251) % 251;
}
