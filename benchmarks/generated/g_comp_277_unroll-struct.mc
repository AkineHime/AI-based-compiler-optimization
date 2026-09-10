// generated: composite unroll+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 8) * 5);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 36; bb.y0 = 25; bb.x1 = 94; bb.y1 = 58;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(1500000);
    return ((s % 251) + 251) % 251;
}
