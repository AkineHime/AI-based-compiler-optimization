// generated: composite struct+cse+licm+cf
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 13; bb.y0 = 21; bb.x1 = 71; bb.y1 = 55;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 36) % 3571;
        int c1 = (x * 36) % 3571;
        int c2 = (x * 36) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 115 * 115 + 19 * 116 + 116 * 115 * 19;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 16;
        int q = 15;
        int r = 17;
        acc = acc + q * r + p * q + p * q * r + r * r * p + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(300000);
    s = s + part2(3400000);
    s = s + part3(366666);
    return ((s % 251) + 251) % 251;
}
