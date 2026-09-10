// generated: composite cse+cse+neutral

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 65) % 10007;
        int c1 = (x * 65) % 10007;
        int c2 = (x * 65) % 10007;
        int c3 = (x * 65) % 10007;
        int c4 = (x * 65) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 42) % 10007;
        int c1 = (x * 42) % 10007;
        int c2 = (x * 42) % 10007;
        acc = acc + c0 + c1 + c2;
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
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
