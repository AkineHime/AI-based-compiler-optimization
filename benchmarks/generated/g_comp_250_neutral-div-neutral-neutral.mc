// generated: composite neutral+div+neutral+neutral

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
        int u = 54945;
        int v = 64908;
        acc = acc + 529217994 / u + 790999200 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(750000);
    s = s + part2(3000000);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
