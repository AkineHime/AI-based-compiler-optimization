// generated: composite struct+branch+cf+unroll
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 7; bb.y0 = 35; bb.x1 = 71; bb.y1 = 88;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 9 + 37 * 38;
        } else {
            acc = acc + i * 39 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 23;
        int q = 29;
        int r = 4;
        acc = acc + q * p * q + p * p + p * q * r + p * q + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 3 - (i - (i / 4) * 8);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1500000);
    s = s + part1(5200000);
    s = s + part2(400000);
    s = s + part3(3000000);
    return ((s % 251) + 251) % 251;
}
