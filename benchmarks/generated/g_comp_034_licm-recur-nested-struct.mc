// generated: composite licm+recur+nested+struct
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 1;
}
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 71 * 101 + 71 * 71 + 71 * 101 * 81 + 101 * 81 * 71;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(320);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 24) {
            inner = inner + j * 21 + i * 14;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 5; bb.y0 = 16; bb.x1 = 75; bb.y1 = 87;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(6000);
    s = s + part2(60000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
