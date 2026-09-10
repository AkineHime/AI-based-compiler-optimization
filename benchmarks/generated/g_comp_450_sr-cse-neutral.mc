// generated: composite sr+cse+neutral

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 31 + 4;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 51) % 6997;
        int c1 = (x * 51) % 6997;
        int c2 = (x * 51) % 6997;
        int c3 = (x * 51) % 6997;
        int c4 = (x * 51) % 6997;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(500000);
    s = s + part2(1133333);
    return ((s % 251) + 251) % 251;
}
