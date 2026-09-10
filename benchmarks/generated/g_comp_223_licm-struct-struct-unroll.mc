// generated: composite licm+struct+struct+unroll
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 145 * 145 + 166 * 166 + 166 * 182 + 145 * 182 * 166 + 166 * 145;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 33; bb.y0 = 8; bb.x1 = 73; bb.y1 = 62;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 33; bb.y0 = 4; bb.x1 = 95; bb.y1 = 58;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 9) * 6);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(600000);
    s = s + part1(366666);
    s = s + part2(366666);
    s = s + part3(550000);
    return ((s % 251) + 251) % 251;
}
