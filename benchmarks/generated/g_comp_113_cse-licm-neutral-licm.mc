// generated: composite cse+licm+neutral+licm

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 21) % 4093;
        int c1 = (x * 21) % 4093;
        int c2 = (x * 21) % 4093;
        int c3 = (x * 21) % 4093;
        int c4 = (x * 21) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 61 * 23 + 61 * 171 + 61 * 171 * 23 + 61 * 61 + 23 * 61;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 45 * 77 + 45 * 77 * 188 + 77 * 77 + 188 * 188 + 188 * 45;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(2000000);
    s = s + part2(666666);
    s = s + part3(2000000);
    return ((s % 251) + 251) % 251;
}
