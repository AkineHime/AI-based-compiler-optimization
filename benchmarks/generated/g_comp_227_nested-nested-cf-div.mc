// generated: composite nested+nested+cf+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 9 + i * 17;
            j = j + 1;
        }
        acc = acc + inner;
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
        while (j < 16) {
            inner = inner + j * 5 + i * 3;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 10;
        int q = 18;
        int r = 16;
        acc = acc + p * q * r + p * p + q * p * q + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 67292;
        int v = 99975;
        acc = acc + 879990488 / u + 133048363 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(130769);
    s = s + part1(130769);
    s = s + part2(366666);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
