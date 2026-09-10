// generated: composite branch+cse+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 7 + 17 * 28;
        } else {
            acc = acc + i * 40 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 54) % 3571;
        int c1 = (x * 54) % 3571;
        int c2 = (x * 54) % 3571;
        int c3 = (x * 54) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 40 + 15 * 15;
        } else {
            acc = acc + i * 16 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(850000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
