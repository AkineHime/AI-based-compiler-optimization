// generated: composite cf+struct+nested+cse
struct __Box { int x0; int y0; int x1; int y1; };

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 40;
        int q = 40;
        int r = 16;
        acc = acc + r * r * p + q * p * q + p * p + p * q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 2; bb.y0 = 21; bb.x1 = 66; bb.y1 = 58;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 24 + i * 26;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 25) % 4093;
        int c1 = (x * 25) % 4093;
        int c2 = (x * 25) % 4093;
        int c3 = (x * 25) % 4093;
        int c4 = (x * 25) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(2600000);
    s = s + part2(60000);
    s = s + part3(1000000);
    return ((s % 251) + 251) % 251;
}
