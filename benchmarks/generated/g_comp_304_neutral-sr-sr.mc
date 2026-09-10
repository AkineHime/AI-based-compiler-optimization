// generated: composite neutral+sr+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 57 + 7;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 + i * 11 + 2;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(1100000);
    s = s + part2(2000000);
    return ((s % 251) + 251) % 251;
}
