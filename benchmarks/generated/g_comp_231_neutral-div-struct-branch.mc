// generated: composite neutral+div+struct+branch
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 46567;
        int v = 73462;
        acc = acc + 1233623765 / u + 1160242880 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 25; bb.y0 = 20; bb.x1 = 84; bb.y1 = 63;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 27 + 25 * 24;
        } else {
            acc = acc + i * 38 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(400000);
    s = s + part2(400000);
    s = s + part3(1600000);
    return ((s % 251) + 251) % 251;
}
