// generated: composite cse+branch+sr+div

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 75) % 4093;
        int c1 = (x * 75) % 4093;
        int c2 = (x * 75) % 4093;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 17 + 32 * 26;
        } else {
            acc = acc + i * 3 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 57 + i * 3 + 2;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 72448;
        int v = 70808;
        acc = acc + 1540348252 / u + 1735275709 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(366666);
    s = s + part2(3400000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
