// generated: composite cse+unroll+branch

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 48) % 6997;
        int c1 = (x * 48) % 6997;
        int c2 = (x * 48) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 - (i - (i / 6) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 16 + 18 * 14;
        } else {
            acc = acc + i * 12 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(800000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
