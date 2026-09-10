// generated: composite cse+licm+licm+div

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 80) % 6997;
        int c1 = (x * 80) % 6997;
        int c2 = (x * 80) % 6997;
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
        acc = acc + 91 * 91 + 147 * 91 + 91 * 147 + 52 * 52 + 147 * 147 + 52 * 147 * 91;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 73 * 103 + 103 * 42 + 103 * 103 + 42 * 42 + 73 * 73 + 103 * 73;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 79587;
        int v = 93141;
        acc = acc + 719992066 / u + 1729428462 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1600000);
    s = s + part2(800000);
    s = s + part3(750000);
    return ((s % 251) + 251) % 251;
}
