// generated: composite sr+cse+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 3 + 6;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 82) % 3571;
        int c1 = (x * 82) % 3571;
        int c2 = (x * 82) % 3571;
        int c3 = (x * 82) % 3571;
        int c4 = (x * 82) % 3571;
        acc = acc + c0 + c1 + c2 + c3 + c4;
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
            acc = acc + i * 27 + 36 * 7;
        } else {
            acc = acc + i * 4 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(600000);
    s = s + part1(300000);
    s = s + part2(1133333);
    return ((s % 251) + 251) % 251;
}
