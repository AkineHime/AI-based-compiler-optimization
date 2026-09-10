// generated: composite cf+licm+sr+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 39;
        int q = 37;
        int r = 15;
        acc = acc + q * p * q + p * p + p * q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 63 * 63 + 134 * 197 * 63 + 63 * 197 + 197 * 197 + 197 * 63;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 57 + i * 7 + 9;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 118 * 121 + 181 * 181 + 118 * 118 + 118 * 121 * 181;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(5200000);
    s = s + part2(400000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
