// generated: composite licm+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 166 * 123 + 100 * 123 * 166 + 100 * 100;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 + i * 11 + i * 17 + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(2000000);
    return ((s % 251) + 251) % 251;
}
