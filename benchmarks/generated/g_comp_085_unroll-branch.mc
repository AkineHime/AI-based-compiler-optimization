// generated: composite unroll+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 6 - (i - (i / 3) * 5);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 32 + 37 * 21;
        } else {
            acc = acc + i * 38 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(3000000);
    return ((s % 251) + 251) % 251;
}
