// generated: composite cse+div+branch

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 61) % 4093;
        int c1 = (x * 61) % 4093;
        int c2 = (x * 61) % 4093;
        int c3 = (x * 61) % 4093;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 90638;
        int v = 88103;
        acc = acc + 1953517691 / u + 1019737110 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 14 + 30 * 38;
        } else {
            acc = acc + i * 25 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(366666);
    return ((s % 251) + 251) % 251;
}
