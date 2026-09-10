// generated: composite struct+licm+struct+cf
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 40; bb.y0 = 24; bb.x1 = 74; bb.y1 = 79;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 197 * 197 + 197 * 155 + 187 * 187 + 155 * 155;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 34; bb.y0 = 31; bb.x1 = 57; bb.y1 = 90;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 29;
        int q = 20;
        int r = 36;
        acc = acc + q * p * q + r * r * p + p * p + q * r + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(3000000);
    s = s + part2(800000);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
