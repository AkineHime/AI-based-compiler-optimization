// generated: composite sr+unroll+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 + i * 3 + 9;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 9 - (i - (i / 8) * 3);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 45258;
        int v = 99020;
        acc = acc + 1113114279 / u + 1081890189 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(300000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
