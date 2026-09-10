// generated: composite cf+struct+cf+unroll
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 22;
        int q = 37;
        int r = 22;
        acc = acc + p * q * r + q * r + p * p + r * r * p + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 29; bb.y0 = 35; bb.x1 = 83; bb.y1 = 96;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 31;
        int q = 3;
        int r = 7;
        acc = acc + r * r * p + p * p + p * q + q * r + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 3 - (i - (i / 6) * 5);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(666666);
    s = s + part2(300000);
    s = s + part3(1700000);
    return ((s % 251) + 251) % 251;
}
