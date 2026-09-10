// generated: composite branch+div+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 23 + 8 * 21;
        } else {
            acc = acc + i * 6 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 55489;
        int v = 49912;
        acc = acc + 476418098 / u + 1451707995 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 61 * 129 + 129 * 61 + 61 * 61 + 129 * 18 * 61 + 129 * 129;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(400000);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
