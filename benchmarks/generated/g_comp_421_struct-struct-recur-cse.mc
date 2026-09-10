// generated: composite struct+struct+recur+cse
struct __Box { int x0; int y0; int x1; int y1; };
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 19; bb.y0 = 38; bb.x1 = 88; bb.y1 = 75;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 31; bb.y0 = 10; bb.x1 = 84; bb.y1 = 87;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec2(320);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 94) % 6997;
        int c1 = (x * 94) % 6997;
        int c2 = (x * 94) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(1500000);
    s = s + part2(6153);
    s = s + part3(1733333);
    return ((s % 251) + 251) % 251;
}
