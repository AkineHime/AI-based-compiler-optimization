// generated: composite div+div+cf+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 69999;
        int v = 40322;
        acc = acc + 940524987 / u + 1218438285 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 53707;
        int v = 74628;
        acc = acc + 1191544384 / u + 1611584306 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 3;
        int q = 36;
        int r = 3;
        acc = acc + p * q * r + q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 10 + 19 * 29;
        } else {
            acc = acc + i * 23 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1300000);
    s = s + part2(3000000);
    s = s + part3(1600000);
    return ((s % 251) + 251) % 251;
}
