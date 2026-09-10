// generated: composite div+cse+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 63873;
        int v = 68315;
        acc = acc + 661615907 / u + 612550663 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 62) % 7919;
        int c1 = (x * 62) % 7919;
        int c2 = (x * 62) % 7919;
        int c3 = (x * 62) % 7919;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 98733;
        int v = 50629;
        acc = acc + 223442442 / u + 1887400447 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(500000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
