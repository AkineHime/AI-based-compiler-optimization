// generated: composite struct+recur
struct __Box { int x0; int y0; int x1; int y1; };
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 37; bb.y0 = 29; bb.x1 = 98; bb.y1 = 60;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(240);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(4000);
    return ((s % 251) + 251) % 251;
}
