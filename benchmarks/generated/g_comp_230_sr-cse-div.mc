// generated: composite sr+cse+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 31 + i * 5 + i * 7 + 8;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 21) % 7919;
        int c1 = (x * 21) % 7919;
        int c2 = (x * 21) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 52046;
        int v = 64178;
        acc = acc + 110319977 / u + 1028977220 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(400000);
    s = s + part2(750000);
    return ((s % 251) + 251) % 251;
}
