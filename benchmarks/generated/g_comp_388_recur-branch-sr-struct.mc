// generated: composite recur+branch+sr+struct
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 4;
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
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 33 + 37 * 6;
        } else {
            acc = acc + i * 6 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 + i * 7 + 6;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 25; bb.y0 = 6; bb.x1 = 84; bb.y1 = 63;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(6153);
    s = s + part1(3000000);
    s = s + part2(3000000);
    s = s + part3(1500000);
    return ((s % 251) + 251) % 251;
}
