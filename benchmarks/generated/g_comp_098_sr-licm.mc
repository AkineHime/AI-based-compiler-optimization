// generated: composite sr+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 17 + i * 31 + i * 57 + 8;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 104 * 98 * 47 + 47 * 104 * 98 + 98 * 98 + 47 * 104;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3400000);
    s = s + part1(1100000);
    return ((s % 251) + 251) % 251;
}
