// generated: composite neutral+struct+cse+nested
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
        struct __Box bb;
        bb.x0 = 2; bb.y0 = 26; bb.x1 = 90; bb.y1 = 66;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 21) % 3571;
        int c1 = (x * 21) % 3571;
        int c2 = (x * 21) % 3571;
        int c3 = (x * 21) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 24) {
            inner = inner + j * 5 + i * 17;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(1500000);
    s = s + part2(1733333);
    s = s + part3(60000);
    return ((s % 251) + 251) % 251;
}
