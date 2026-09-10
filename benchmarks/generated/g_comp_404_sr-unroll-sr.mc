// generated: composite sr+unroll+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 31 + 2;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 9 - (i - (i / 5) * 5);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 + i * 7 + i * 31 + 8;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(400000);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
