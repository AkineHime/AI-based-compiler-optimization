// generated: composite unroll+struct+nested+licm
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 2 - (i - (i / 3) * 6);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 7; bb.y0 = 38; bb.x1 = 75; bb.y1 = 70;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 22 + i * 16;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 154 * 154 + 148 * 154 * 124 + 124 * 154 + 124 * 148 * 154 + 124 * 124 + 154 * 124;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(60000);
    s = s + part3(800000);
    return ((s % 251) + 251) % 251;
}
