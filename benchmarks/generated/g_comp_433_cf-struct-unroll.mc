// generated: composite cf+struct+unroll
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 8;
        int q = 36;
        int r = 16;
        acc = acc + r * r * p + q * p * q + p * q + p * q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 26; bb.y0 = 30; bb.x1 = 60; bb.y1 = 95;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 9 - (i - (i / 8) * 3);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(2600000);
    s = s + part2(1600000);
    return ((s % 251) + 251) % 251;
}
