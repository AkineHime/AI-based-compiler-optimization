// generated: composite cse+div

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 71) % 3571;
        int c1 = (x * 71) % 3571;
        int c2 = (x * 71) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 47402;
        int v = 91641;
        acc = acc + 446541040 / u + 1379032117 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1733333);
    s = s + part1(750000);
    return ((s % 251) + 251) % 251;
}
