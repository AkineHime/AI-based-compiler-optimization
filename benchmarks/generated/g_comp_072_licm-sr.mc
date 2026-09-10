// generated: composite licm+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 31 * 31 + 31 * 29 + 158 * 31 + 29 * 158 * 31 + 31 * 158;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 11 + 6;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
