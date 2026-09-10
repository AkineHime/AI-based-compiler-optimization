// generated: composite struct+unroll+div+recur
struct __Box { int x0; int y0; int x1; int y1; };
int rec3(int n) {
    if (n < 2) { return n; }
    return rec3(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 2; bb.y0 = 25; bb.x1 = 60; bb.y1 = 83;
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
        acc = acc + i * 8 - (i - (i / 9) * 9);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 89297;
        int v = 58750;
        acc = acc + 946959440 / u + 942932046 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec3(460);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1500000);
    s = s + part1(1600000);
    s = s + part2(1300000);
    s = s + part3(6000);
    return ((s % 251) + 251) % 251;
}
