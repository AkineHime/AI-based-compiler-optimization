// generated: composite sr+unroll+sr+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 + 9;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 2 - (i - (i / 5) * 6);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 3 + i * 13 + i * 57 + 7;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 22) % 10007;
        int c1 = (x * 22) % 10007;
        int c2 = (x * 22) % 10007;
        int c3 = (x * 22) % 10007;
        int c4 = (x * 22) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(5200000);
    s = s + part2(1600000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
