// generated: composite struct+branch+recur+cf
struct __Box { int x0; int y0; int x1; int y1; };
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 37; bb.y0 = 27; bb.x1 = 71; bb.y1 = 53;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 23 + 33 * 35;
        } else {
            acc = acc + i * 26 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec2(200);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 28;
        int q = 39;
        int r = 22;
        acc = acc + r * r * p + q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(800000);
    s = s + part2(6000);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
