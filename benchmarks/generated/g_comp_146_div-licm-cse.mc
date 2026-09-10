// generated: composite div+licm+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 53711;
        int v = 82017;
        acc = acc + 657314920 / u + 1427751136 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 47 * 28 + 47 * 47 + 47 * 178;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 81) % 7919;
        int c1 = (x * 81) % 7919;
        int c2 = (x * 81) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1300000);
    s = s + part1(400000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
