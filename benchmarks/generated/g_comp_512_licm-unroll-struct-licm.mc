// generated: composite licm+unroll+struct+licm
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 182 * 184 + 182 * 182 + 122 * 182 + 182 * 122 + 184 * 184;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 4 - (i - (i / 3) * 6);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 18; bb.y0 = 29; bb.x1 = 88; bb.y1 = 89;
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
        acc = acc + 86 * 183 + 86 * 166 + 166 * 183 * 86 + 183 * 86 + 86 * 166 * 183 + 183 * 183;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(2000000);
    s = s + part1(1000000);
    s = s + part2(366666);
    s = s + part3(2000000);
    return ((s % 251) + 251) % 251;
}
