// generated: composite sr+sr+unroll+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 17 + i * 11 + i * 31 + 2;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 57 + i * 31 + 7;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 4 - (i - (i / 6) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 45337;
        int v = 93159;
        acc = acc + 1838806793 / u + 228867156 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3400000);
    s = s + part1(3400000);
    s = s + part2(1700000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
