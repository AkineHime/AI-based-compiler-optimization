// generated: composite cse+cf+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 58) % 3571;
        int c1 = (x * 58) % 3571;
        int c2 = (x * 58) % 3571;
        int c3 = (x * 58) % 3571;
        int c4 = (x * 58) % 3571;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 38;
        int q = 23;
        int r = 10;
        acc = acc + p * q * r + p * p + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 18; bb.y0 = 24; bb.x1 = 62; bb.y1 = 94;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(800000);
    s = s + part2(1500000);
    return ((s % 251) + 251) % 251;
}
