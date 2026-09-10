// generated: composite div+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 55435;
        int v = 56234;
        acc = acc + 630210511 / u + 172155499 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 6 + i * 19;
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
    s = s + part1(214285);
    return ((s % 251) + 251) % 251;
}
