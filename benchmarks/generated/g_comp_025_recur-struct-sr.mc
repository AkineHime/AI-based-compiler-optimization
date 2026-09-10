// generated: composite recur+struct+sr
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 5;
}
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(320);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 8; bb.y0 = 32; bb.x1 = 67; bb.y1 = 90;
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
        acc = acc + i * 5 + i * 3 + 7;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(20000);
    s = s + part1(400000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
