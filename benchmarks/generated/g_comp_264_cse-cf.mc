// generated: composite cse+cf

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 39) % 6997;
        int c1 = (x * 39) % 6997;
        int c2 = (x * 39) % 6997;
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
        int p = 33;
        int q = 5;
        int r = 14;
        acc = acc + p * q + r * r * p + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(800000);
    return ((s % 251) + 251) % 251;
}
