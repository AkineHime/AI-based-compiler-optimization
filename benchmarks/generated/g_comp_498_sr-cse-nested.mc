// generated: composite sr+cse+nested

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 31 + i * 5 + 4;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 75) % 4093;
        int c1 = (x * 75) % 4093;
        int c2 = (x * 75) % 4093;
        int c3 = (x * 75) % 4093;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 18 + i * 19;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(2000000);
    s = s + part1(300000);
    s = s + part2(42307);
    return ((s % 251) + 251) % 251;
}
