// generated: composite div+struct+licm
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 82411;
        int v = 60247;
        acc = acc + 705431150 / u + 129107236 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 19; bb.y0 = 10; bb.x1 = 63; bb.y1 = 73;
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
        acc = acc + 174 * 174 + 105 * 105 + 105 * 98 * 174;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1300000);
    s = s + part1(400000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
