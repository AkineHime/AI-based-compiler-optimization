// generated: composite licm+div+sr+neutral

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 48 * 48 + 48 * 64 + 73 * 73;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 63714;
        int v = 98849;
        acc = acc + 107041026 / u + 1033609201 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 3 + i * 5 + i * 11 + 1;
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
    s = s + part0(3000000);
    s = s + part1(750000);
    s = s + part2(3000000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
