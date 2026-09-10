// generated: composite cse+div+branch

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 56) % 4093;
        int c1 = (x * 56) % 4093;
        int c2 = (x * 56) % 4093;
        int c3 = (x * 56) % 4093;
        int c4 = (x * 56) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 81359;
        int v = 50249;
        acc = acc + 1225404059 / u + 722612145 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 16 + 35 * 15;
        } else {
            acc = acc + i * 29 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(1300000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
