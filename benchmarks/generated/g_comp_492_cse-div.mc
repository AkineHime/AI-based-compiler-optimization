// generated: composite cse+div

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 80) % 3571;
        int c1 = (x * 80) % 3571;
        int c2 = (x * 80) % 3571;
        int c3 = (x * 80) % 3571;
        int c4 = (x * 80) % 3571;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 95558;
        int v = 61075;
        acc = acc + 1647874142 / u + 1318463604 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
