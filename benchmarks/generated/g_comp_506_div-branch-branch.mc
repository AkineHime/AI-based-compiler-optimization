// generated: composite div+branch+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 40162;
        int v = 60080;
        acc = acc + 960925454 / u + 1318809020 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 31 + 6 * 5;
        } else {
            acc = acc + i * 12 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 40 + 20 * 36;
        } else {
            acc = acc + i * 27 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(680000);
    s = s + part1(300000);
    s = s + part2(666666);
    return ((s % 251) + 251) % 251;
}
