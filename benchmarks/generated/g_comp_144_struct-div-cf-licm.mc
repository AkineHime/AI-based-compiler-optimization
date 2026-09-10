// generated: composite struct+div+cf+licm
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 3; bb.y0 = 23; bb.x1 = 64; bb.y1 = 84;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 93481;
        int v = 61542;
        acc = acc + 103717014 / u + 1754458665 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 23;
        int q = 30;
        int r = 24;
        acc = acc + p * q * r + q * p * q + r * r * p + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 42 * 42 + 128 * 128 + 148 * 42 + 148 * 128;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(600000);
    return ((s % 251) + 251) % 251;
}
