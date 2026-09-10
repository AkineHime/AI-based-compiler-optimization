// generated: composite cf+cse

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 30;
        int q = 22;
        int r = 7;
        acc = acc + p * p + r * r * p + p * q * r + q * p * q + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 32) % 6997;
        int c1 = (x * 32) % 6997;
        int c2 = (x * 32) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
