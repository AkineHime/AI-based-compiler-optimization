// generated: composite div+unroll+neutral+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 43551;
        int v = 59914;
        acc = acc + 1814694386 / u + 1957112811 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 6 - (i - (i / 4) * 8);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
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
        while (j < 6) {
            inner = inner + j * 9 + i * 3;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(750000);
    s = s + part1(5200000);
    s = s + part2(5200000);
    s = s + part3(214285);
    return ((s % 251) + 251) % 251;
}
