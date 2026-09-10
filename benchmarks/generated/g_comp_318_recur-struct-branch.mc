// generated: composite recur+struct+branch
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 1;
}
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(200);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 22; bb.y0 = 20; bb.x1 = 67; bb.y1 = 67;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 8 + 17 * 5;
        } else {
            acc = acc + i * 8 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(20000);
    s = s + part1(2600000);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
