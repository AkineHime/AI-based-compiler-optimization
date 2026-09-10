// generated: composite struct+licm
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 31; bb.y0 = 9; bb.x1 = 68; bb.y1 = 79;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 186 * 189 * 155 + 155 * 186 * 189 + 189 * 155 + 189 * 189 + 155 * 189;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
