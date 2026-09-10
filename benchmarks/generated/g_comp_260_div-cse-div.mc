// generated: composite div+cse+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 40792;
        int v = 68543;
        acc = acc + 572284795 / u + 915836730 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 69) % 7919;
        int c1 = (x * 69) % 7919;
        int c2 = (x * 69) % 7919;
        int c3 = (x * 69) % 7919;
        int c4 = (x * 69) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 91534;
        int v = 40027;
        acc = acc + 301700405 / u + 590538372 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(500000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
