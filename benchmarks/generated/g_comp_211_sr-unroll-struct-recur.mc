// generated: composite sr+unroll+struct+recur
struct __Box { int x0; int y0; int x1; int y1; };
int rec3(int n) {
    if (n < 2) { return n; }
    return rec3(n - 1) + 5;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 3 + 7;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 4) * 5);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 37; bb.y0 = 10; bb.x1 = 72; bb.y1 = 73;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec3(200);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(1600000);
    s = s + part2(800000);
    s = s + part3(6000);
    return ((s % 251) + 251) % 251;
}
