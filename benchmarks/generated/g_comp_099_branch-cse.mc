// generated: composite branch+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 39 + 23 * 5;
        } else {
            acc = acc + i * 20 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 38) % 4093;
        int c1 = (x * 38) % 4093;
        int c2 = (x * 38) % 4093;
        int c3 = (x * 38) % 4093;
        int c4 = (x * 38) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
