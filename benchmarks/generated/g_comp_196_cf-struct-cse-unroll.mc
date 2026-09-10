// generated: composite cf+struct+cse+unroll
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 4;
        int q = 14;
        int r = 13;
        acc = acc + r * r * p + p * p + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 24; bb.y0 = 5; bb.x1 = 78; bb.y1 = 83;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 69) % 7919;
        int c1 = (x * 69) % 7919;
        int c2 = (x * 69) % 7919;
        int c3 = (x * 69) % 7919;
        int c4 = (x * 69) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 2 - (i - (i / 6) * 6);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(2600000);
    s = s + part2(1733333);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
