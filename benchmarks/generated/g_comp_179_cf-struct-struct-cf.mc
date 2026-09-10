// generated: composite cf+struct+struct+cf
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 26;
        int q = 7;
        int r = 7;
        acc = acc + p * p + r * r * p + p * q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 14; bb.y0 = 31; bb.x1 = 90; bb.y1 = 75;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 32; bb.y0 = 26; bb.x1 = 69; bb.y1 = 90;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 25;
        int q = 39;
        int r = 9;
        acc = acc + p * q + p * p + q * p * q + r * r * p + q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(366666);
    s = s + part2(1133333);
    s = s + part3(1133333);
    return ((s % 251) + 251) % 251;
}
