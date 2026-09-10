// generated: composite div+cse+sr

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 98237;
        int v = 45747;
        acc = acc + 1433953103 / u + 1972874291 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 27) % 3571;
        int c1 = (x * 27) % 3571;
        int c2 = (x * 27) % 3571;
        int c3 = (x * 27) % 3571;
        int c4 = (x * 27) % 3571;
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
        acc = acc + i * 17 + 6;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(300000);
    return ((s % 251) + 251) % 251;
}
