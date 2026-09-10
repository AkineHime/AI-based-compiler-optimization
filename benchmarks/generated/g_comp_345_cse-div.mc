// generated: composite cse+div

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 81) % 7919;
        int c1 = (x * 81) % 7919;
        int c2 = (x * 81) % 7919;
        int c3 = (x * 81) % 7919;
        int c4 = (x * 81) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 55375;
        int v = 65934;
        acc = acc + 1940317130 / u + 575914812 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(850000);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
