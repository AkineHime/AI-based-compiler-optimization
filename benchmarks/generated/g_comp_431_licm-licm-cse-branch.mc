// generated: composite licm+licm+cse+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 61 * 61 + 140 * 199 * 61 + 61 * 140 + 140 * 199 + 140 * 61 + 199 * 61 * 140;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 162 * 162 + 162 * 197 + 197 * 197 + 162 * 130 + 197 * 162;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 73) % 7919;
        int c1 = (x * 73) % 7919;
        int c2 = (x * 73) % 7919;
        int c3 = (x * 73) % 7919;
        int c4 = (x * 73) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 31 + 3 * 13;
        } else {
            acc = acc + i * 39 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1600000);
    s = s + part2(533333);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
