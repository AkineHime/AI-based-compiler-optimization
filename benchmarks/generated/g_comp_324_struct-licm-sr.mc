// generated: composite struct+licm+sr
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 19; bb.y0 = 9; bb.x1 = 73; bb.y1 = 72;
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
        acc = acc + 177 * 50 + 177 * 177 + 177 * 127 + 177 * 50 * 127 + 50 * 127 * 177 + 127 * 127;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 17 + 9;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(1600000);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
