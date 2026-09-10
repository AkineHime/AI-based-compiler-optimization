// generated: composite cf+branch+licm+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 14;
        int q = 30;
        int r = 4;
        acc = acc + p * p + q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 15 + 40 * 34;
        } else {
            acc = acc + i * 24 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 98 * 98 + 81 * 98 * 27 + 81 * 98;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 24; bb.y0 = 16; bb.x1 = 59; bb.y1 = 55;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(400000);
    s = s + part2(5200000);
    s = s + part3(2600000);
    return ((s % 251) + 251) % 251;
}
