// generated: composite branch+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 5 + 31 * 22;
        } else {
            acc = acc + i * 40 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 37 * 38 + 37 * 114 + 38 * 38 + 37 * 37 + 114 * 37;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(2000000);
    return ((s % 251) + 251) % 251;
}
