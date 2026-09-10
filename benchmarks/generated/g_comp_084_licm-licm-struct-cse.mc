// generated: composite licm+licm+struct+cse
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 41 * 135 + 45 * 41 + 41 * 45 + 45 * 45 + 41 * 135 * 45 + 41 * 41;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 39 * 146 * 139 + 139 * 39 + 139 * 139 + 146 * 139 + 146 * 146;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 19; bb.y0 = 13; bb.x1 = 50; bb.y1 = 66;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 18) % 7919;
        int c1 = (x * 18) % 7919;
        int c2 = (x * 18) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(400000);
    s = s + part2(800000);
    s = s + part3(1733333);
    return ((s % 251) + 251) % 251;
}
