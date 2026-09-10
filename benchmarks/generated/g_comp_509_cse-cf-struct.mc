// generated: composite cse+cf+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 68) % 4093;
        int c1 = (x * 68) % 4093;
        int c2 = (x * 68) % 4093;
        int c3 = (x * 68) % 4093;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 23;
        int q = 19;
        int r = 5;
        acc = acc + q * r + r * r * p + p * q * r + q * p * q + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 24; bb.y0 = 37; bb.x1 = 76; bb.y1 = 75;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(366666);
    s = s + part2(366666);
    return ((s % 251) + 251) % 251;
}
