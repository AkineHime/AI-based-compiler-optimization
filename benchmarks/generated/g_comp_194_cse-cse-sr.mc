// generated: composite cse+cse+sr

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 32) % 7919;
        int c1 = (x * 32) % 7919;
        int c2 = (x * 32) % 7919;
        int c3 = (x * 32) % 7919;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 76) % 7919;
        int c1 = (x * 76) % 7919;
        int c2 = (x * 76) % 7919;
        int c3 = (x * 76) % 7919;
        int c4 = (x * 76) % 7919;
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
        acc = acc + i * 5 + i * 7 + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1000000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
