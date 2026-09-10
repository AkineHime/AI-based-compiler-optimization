// generated: composite branch+struct+cse+branch
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 27 + 3 * 7;
        } else {
            acc = acc + i * 4 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 34; bb.y0 = 37; bb.x1 = 89; bb.y1 = 89;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 22) % 3571;
        int c1 = (x * 22) % 3571;
        int c2 = (x * 22) % 3571;
        int c3 = (x * 22) % 3571;
        int c4 = (x * 22) % 3571;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 37 + 21 * 32;
        } else {
            acc = acc + i * 28 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(1133333);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
