// generated: composite div+struct
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 49759;
        int v = 73628;
        acc = acc + 1234399081 / u + 474628564 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 35; bb.y0 = 11; bb.x1 = 74; bb.y1 = 58;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(800000);
    return ((s % 251) + 251) % 251;
}
