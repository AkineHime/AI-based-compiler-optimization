// generated: composite recur+struct+recur+unroll
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 2;
}
struct __Box { int x0; int y0; int x1; int y1; };
int rec2(int n) {
    if (n < 2) { return n; }
    return rec2(n - 1) + 2;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(120);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 35; bb.y0 = 11; bb.x1 = 81; bb.y1 = 61;
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
        acc = acc + rec2(120);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 2 - (i - (i / 9) * 9);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(20000);
    s = s + part1(1500000);
    s = s + part2(20000);
    s = s + part3(1600000);
    return ((s % 251) + 251) % 251;
}
