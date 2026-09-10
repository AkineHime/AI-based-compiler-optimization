// generated: composite sr+branch+div+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 31 + 4;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 19 + 6 * 17;
        } else {
            acc = acc + i * 13 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 90539;
        int v = 44134;
        acc = acc + 1454668453 / u + 922765779 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 30; bb.y0 = 15; bb.x1 = 56; bb.y1 = 76;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(1600000);
    s = s + part2(1300000);
    s = s + part3(1500000);
    return ((s % 251) + 251) % 251;
}
