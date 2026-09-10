// generated: composite sr+recur+div+licm
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 7 + i * 17 + i * 31 + 7;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(60);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 71320;
        int v = 41675;
        acc = acc + 286591141 / u + 275640065 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 164 * 66 + 66 * 129 * 164 + 66 * 66 + 66 * 164 + 129 * 164 * 66 + 66 * 129;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(600000);
    s = s + part1(4000);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
