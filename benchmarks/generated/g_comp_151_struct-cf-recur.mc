// generated: composite struct+cf+recur
struct __Box { int x0; int y0; int x1; int y1; };
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 18; bb.y0 = 2; bb.x1 = 53; bb.y1 = 56;
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
        int p = 31;
        int q = 34;
        int r = 10;
        acc = acc + p * q * r + r * r * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec2(460);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1500000);
    s = s + part1(3000000);
    s = s + part2(6000);
    return ((s % 251) + 251) % 251;
}
