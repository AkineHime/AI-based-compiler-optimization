// generated: composite cse+cf

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 79) % 7919;
        int c1 = (x * 79) % 7919;
        int c2 = (x * 79) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 15;
        int q = 31;
        int r = 38;
        acc = acc + p * q * r + p * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(1133333);
    return ((s % 251) + 251) % 251;
}
