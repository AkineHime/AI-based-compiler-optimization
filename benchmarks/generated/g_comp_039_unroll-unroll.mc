// generated: composite unroll+unroll

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 5) * 6);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 4) * 9);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1700000);
    s = s + part1(1000000);
    return ((s % 251) + 251) % 251;
}
