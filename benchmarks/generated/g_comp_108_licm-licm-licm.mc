// generated: composite licm+licm+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 35 * 176 + 176 * 176 + 35 * 35 + 35 * 116;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 197 * 180 * 198 + 198 * 197 + 180 * 198 * 197 + 197 * 180;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 12 * 12 + 176 * 133 * 12 + 12 * 176 + 12 * 176 * 133 + 133 * 12;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(1100000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
