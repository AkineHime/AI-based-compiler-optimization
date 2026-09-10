// generated: composite struct+cf
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 13; bb.y0 = 30; bb.x1 = 85; bb.y1 = 59;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 12;
        int q = 4;
        int r = 20;
        acc = acc + r * r * p + p * q + q * p * q + p * q * r + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1500000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
