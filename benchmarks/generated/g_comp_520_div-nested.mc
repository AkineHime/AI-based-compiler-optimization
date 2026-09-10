// generated: composite div+nested

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 86106;
        int v = 89591;
        acc = acc + 1529680548 / u + 1713786218 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 16 + i * 13;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1300000);
    s = s + part1(214285);
    return ((s % 251) + 251) % 251;
}
