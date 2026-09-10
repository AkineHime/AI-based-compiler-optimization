// generated: composite div+div+neutral+neutral

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 40892;
        int v = 43563;
        acc = acc + 1524611294 / u + 916724473 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 54931;
        int v = 79257;
        acc = acc + 1442044463 / u + 476217218 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
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
    s = s + part0(750000);
    s = s + part1(1300000);
    s = s + part2(3000000);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
