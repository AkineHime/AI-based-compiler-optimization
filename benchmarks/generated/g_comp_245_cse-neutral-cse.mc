// generated: composite cse+neutral+cse

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 52) % 6997;
        int c1 = (x * 52) % 6997;
        int c2 = (x * 52) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 20) % 7919;
        int c1 = (x * 20) % 7919;
        int c2 = (x * 20) % 7919;
        int c3 = (x * 20) % 7919;
        int c4 = (x * 20) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(533333);
    s = s + part1(5200000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
