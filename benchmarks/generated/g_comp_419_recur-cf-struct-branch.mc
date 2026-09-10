// generated: composite recur+cf+struct+branch
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(60);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 23;
        int q = 31;
        int r = 39;
        acc = acc + q * p * q + p * q * r + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 7; bb.y0 = 17; bb.x1 = 80; bb.y1 = 55;
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
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 38 + 5 * 10;
        } else {
            acc = acc + i * 31 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(4000);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
