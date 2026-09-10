// generated: composite cf+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 30;
        int q = 40;
        int r = 12;
        acc = acc + p * q * r + p * q + p * p + q * p * q + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 33; bb.y0 = 19; bb.x1 = 62; bb.y1 = 57;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1133333);
    s = s + part1(366666);
    return ((s % 251) + 251) % 251;
}
