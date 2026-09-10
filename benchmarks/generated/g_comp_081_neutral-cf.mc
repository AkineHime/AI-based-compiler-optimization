// generated: composite neutral+cf

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 16;
        int q = 26;
        int r = 5;
        acc = acc + q * p * q + p * q + q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
