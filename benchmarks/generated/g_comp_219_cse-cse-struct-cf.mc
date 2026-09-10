// generated: composite cse+cse+struct+cf
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 47) % 3571;
        int c1 = (x * 47) % 3571;
        int c2 = (x * 47) % 3571;
        int c3 = (x * 47) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 65) % 4093;
        int c1 = (x * 65) % 4093;
        int c2 = (x * 65) % 4093;
        int c3 = (x * 65) % 4093;
        int c4 = (x * 65) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 12; bb.y0 = 30; bb.x1 = 78; bb.y1 = 61;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 19;
        int q = 10;
        int r = 10;
        acc = acc + q * p * q + q * r + r * r * p + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(533333);
    s = s + part2(400000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
