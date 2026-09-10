// generated: composite unroll+recur+div+struct
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 2;
}
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 5) * 4);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(100);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 86890;
        int v = 99044;
        acc = acc + 846393601 / u + 1730057966 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 40; bb.y0 = 27; bb.x1 = 98; bb.y1 = 85;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(4000);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
