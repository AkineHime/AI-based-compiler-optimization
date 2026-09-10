// generated: composite licm+cse+neutral+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 20 * 82 + 45 * 45 + 82 * 45 * 20 + 20 * 20;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 97) % 4093;
        int c1 = (x * 97) % 4093;
        int c2 = (x * 97) % 4093;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
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
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 23) % 3571;
        int c1 = (x * 23) % 3571;
        int c2 = (x * 23) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(533333);
    s = s + part2(3000000);
    s = s + part3(1000000);
    return ((s % 251) + 251) % 251;
}
