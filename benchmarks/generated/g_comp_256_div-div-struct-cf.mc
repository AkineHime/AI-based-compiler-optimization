// generated: composite div+div+struct+cf
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 98496;
        int v = 73624;
        acc = acc + 688001563 / u + 1377949788 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 98494;
        int v = 55796;
        acc = acc + 1032467930 / u + 1098856084 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 15; bb.y0 = 10; bb.x1 = 85; bb.y1 = 91;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 26;
        int q = 19;
        int r = 15;
        acc = acc + q * r + p * q * r + p * p + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1300000);
    s = s + part1(400000);
    s = s + part2(400000);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
