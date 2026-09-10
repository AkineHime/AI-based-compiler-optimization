// generated: composite licm+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 71 * 71 + 66 * 66 + 66 * 71 * 31 + 31 * 71 + 31 * 66 + 31 * 66 * 71;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 13; bb.y0 = 15; bb.x1 = 94; bb.y1 = 55;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1500000);
    return ((s % 251) + 251) % 251;
}
