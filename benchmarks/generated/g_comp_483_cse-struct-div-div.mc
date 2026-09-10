// generated: composite cse+struct+div+div
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 66) % 6997;
        int c1 = (x * 66) % 6997;
        int c2 = (x * 66) % 6997;
        int c3 = (x * 66) % 6997;
        int c4 = (x * 66) % 6997;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 40; bb.y0 = 5; bb.x1 = 90; bb.y1 = 68;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 85055;
        int v = 91646;
        acc = acc + 386398288 / u + 1378549210 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 58603;
        int v = 63847;
        acc = acc + 1891340041 / u + 1754095213 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
