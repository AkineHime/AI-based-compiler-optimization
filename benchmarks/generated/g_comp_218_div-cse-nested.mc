// generated: composite div+cse+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 71032;
        int v = 48317;
        acc = acc + 403436329 / u + 244122581 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 29) % 10007;
        int c1 = (x * 29) % 10007;
        int c2 = (x * 29) % 10007;
        int c3 = (x * 29) % 10007;
        int c4 = (x * 29) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
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
        while (j < 10) {
            inner = inner + j * 20 + i * 25;
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
    s = s + part1(300000);
    s = s + part2(40000);
    return ((s % 251) + 251) % 251;
}
