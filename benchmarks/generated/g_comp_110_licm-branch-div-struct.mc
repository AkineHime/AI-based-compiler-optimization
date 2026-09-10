// generated: composite licm+branch+div+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 83 * 83 + 153 * 83 + 83 * 114 * 153 + 153 * 153;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 18 + 9 * 3;
        } else {
            acc = acc + i * 9 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 91883;
        int v = 91842;
        acc = acc + 1606263638 / u + 1324949583 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 16; bb.y0 = 7; bb.x1 = 98; bb.y1 = 60;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(5200000);
    s = s + part1(3000000);
    s = s + part2(400000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
