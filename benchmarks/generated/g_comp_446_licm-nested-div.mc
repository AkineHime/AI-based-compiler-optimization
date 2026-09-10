// generated: composite licm+nested+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 66 * 71 + 174 * 174 + 66 * 71 * 174 + 66 * 174 + 71 * 174 * 66;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 24) {
            inner = inner + j * 12 + i * 2;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 66662;
        int v = 74297;
        acc = acc + 1151168385 / u + 820380260 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(114285);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
