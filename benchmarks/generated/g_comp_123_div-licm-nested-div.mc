// generated: composite div+licm+nested+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 90926;
        int v = 63600;
        acc = acc + 1589334858 / u + 501892875 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 132 * 61 * 90 + 132 * 132 + 90 * 132 + 90 * 90 + 61 * 61;
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
            inner = inner + j * 14 + i * 27;
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
        int u = 57488;
        int v = 47370;
        acc = acc + 538032083 / u + 1437310369 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(3000000);
    s = s + part2(214285);
    s = s + part3(750000);
    return ((s % 251) + 251) % 251;
}
