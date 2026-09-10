// generated: composite branch+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 6 + 13 * 17;
        } else {
            acc = acc + i * 30 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 31 + i * 23 + i * 7 + 4;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(800000);
    return ((s % 251) + 251) % 251;
}
