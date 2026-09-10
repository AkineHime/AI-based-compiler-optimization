// generated: composite struct+branch+branch+recur
struct __Box { int x0; int y0; int x1; int y1; };
int rec3(int n) {
    if (n < 2) { return n; }
    return rec3(n - 1) + 1;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 27; bb.y0 = 21; bb.x1 = 75; bb.y1 = 86;
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
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 25 + 25 * 24;
        } else {
            acc = acc + i * 30 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 8 + 25 * 15;
        } else {
            acc = acc + i * 33 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec3(100);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(300000);
    s = s + part2(366666);
    s = s + part3(4000);
    return ((s % 251) + 251) % 251;
}
