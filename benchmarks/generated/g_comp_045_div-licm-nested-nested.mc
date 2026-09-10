// generated: composite div+licm+nested+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 56020;
        int v = 84634;
        acc = acc + 338772957 / u + 179737784 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 64 * 33 + 64 * 99 * 33 + 33 * 33 + 33 * 64 + 64 * 64 + 99 * 99;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 15 + i * 16;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 24) {
            inner = inner + j * 18 + i * 3;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(114285);
    s = s + part3(60000);
    return ((s % 251) + 251) % 251;
}
