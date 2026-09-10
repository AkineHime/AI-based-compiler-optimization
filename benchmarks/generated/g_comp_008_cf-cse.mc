// generated: composite cf+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 4;
        int q = 7;
        int r = 31;
        acc = acc + q * p * q + r * r * p + p * q + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 74) % 6997;
        int c1 = (x * 74) % 6997;
        int c2 = (x * 74) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
