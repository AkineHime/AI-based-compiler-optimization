// generated: composite struct+cse+branch+div
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 32; bb.y0 = 30; bb.x1 = 99; bb.y1 = 87;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 48) % 10007;
        int c1 = (x * 48) % 10007;
        int c2 = (x * 48) % 10007;
        int c3 = (x * 48) % 10007;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 15 + 33 * 40;
        } else {
            acc = acc + i * 35 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 51088;
        int v = 55264;
        acc = acc + 257386441 / u + 855440331 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(850000);
    s = s + part2(1133333);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
