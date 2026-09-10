// generated: composite div+div+cse+nested

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 94719;
        int v = 86528;
        acc = acc + 1098936168 / u + 1157572617 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 65167;
        int v = 76189;
        acc = acc + 1508727892 / u + 147864497 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 18) % 10007;
        int c1 = (x * 18) % 10007;
        int c2 = (x * 18) % 10007;
        int c3 = (x * 18) % 10007;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 22 + i * 13;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(850000);
    s = s + part3(40000);
    return ((s % 251) + 251) % 251;
}
