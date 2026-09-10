// generated: composite branch+neutral+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 5 + 7 * 14;
        } else {
            acc = acc + i * 28 - (i - (i / 5) * 5);
        }
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
    int i = 0;
    while (i < reps) {
        acc = acc + 111 * 69 * 167 + 111 * 111 + 167 * 167;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(3000000);
    s = s + part2(800000);
    return ((s % 251) + 251) % 251;
}
