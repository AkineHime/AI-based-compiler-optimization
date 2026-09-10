// generated: composite cf+neutral

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 39;
        int q = 30;
        int r = 11;
        acc = acc + p * q * r + q * p * q + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(5200000);
    return ((s % 251) + 251) % 251;
}
