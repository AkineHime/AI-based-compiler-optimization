// generated: composite sr+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 31 + i * 17 + 1;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 72 * 125 * 182 + 72 * 72 + 182 * 125 + 182 * 72 + 125 * 182;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(800000);
    return ((s % 251) + 251) % 251;
}
