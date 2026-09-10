// generated: composite sr+cse+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 + i * 57 + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 89) % 6997;
        int c1 = (x * 89) % 6997;
        int c2 = (x * 89) % 6997;
        int c3 = (x * 89) % 6997;
        int c4 = (x * 89) % 6997;
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
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 10 + 24 * 30;
        } else {
            acc = acc + i * 5 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(1733333);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
