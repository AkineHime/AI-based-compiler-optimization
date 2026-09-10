// generated: composite branch+nested+cf+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 4 + 37 * 37;
        } else {
            acc = acc + i * 39 - (i - (i / 5) * 5);
        }
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
        while (j < 24) {
            inner = inner + j * 12 + i * 7;
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
        int p = 3;
        int q = 8;
        int r = 37;
        acc = acc + q * p * q + p * q + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 69) % 4093;
        int c1 = (x * 69) % 4093;
        int c2 = (x * 69) % 4093;
        int c3 = (x * 69) % 4093;
        int c4 = (x * 69) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(76923);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
