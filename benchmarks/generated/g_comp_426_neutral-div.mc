// generated: composite neutral+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 88108;
        int v = 60373;
        acc = acc + 897113335 / u + 1249288688 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(1300000);
    return ((s % 251) + 251) % 251;
}
