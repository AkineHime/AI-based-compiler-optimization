// generated: composite cf+neutral+nested+cf

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 30;
        int q = 3;
        int r = 3;
        acc = acc + p * q * r + p * p + q * r + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 17 + i * 28;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 3;
        int q = 21;
        int r = 4;
        acc = acc + q * p * q + r * r * p + p * q + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(300000);
    s = s + part2(40000);
    s = s + part3(666666);
    return ((s % 251) + 251) % 251;
}
