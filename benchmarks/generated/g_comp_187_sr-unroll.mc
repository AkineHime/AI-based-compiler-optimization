// generated: composite sr+unroll

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 13 + i * 57 + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 9 - (i - (i / 3) * 4);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(600000);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
