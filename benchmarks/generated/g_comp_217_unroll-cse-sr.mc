// generated: composite unroll+cse+sr

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 2 - (i - (i / 7) * 4);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 61) % 7919;
        int c1 = (x * 61) % 7919;
        int c2 = (x * 61) % 7919;
        int c3 = (x * 61) % 7919;
        int c4 = (x * 61) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 11 + i * 5 + 8;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(1000000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
