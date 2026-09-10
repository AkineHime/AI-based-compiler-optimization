// generated: composite div+neutral+div+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 64424;
        int v = 78616;
        acc = acc + 438367699 / u + 948594662 / v + i / (u - (u / 100) * 100 + 1);
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

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 54740;
        int v = 64795;
        acc = acc + 467198095 / u + 1180518597 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 87) % 4093;
        int c1 = (x * 87) % 4093;
        int c2 = (x * 87) % 4093;
        int c3 = (x * 87) % 4093;
        int c4 = (x * 87) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(366666);
    s = s + part2(400000);
    s = s + part3(850000);
    return ((s % 251) + 251) % 251;
}
