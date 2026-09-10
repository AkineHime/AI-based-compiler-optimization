// generated: composite struct+recur+cse+branch
struct __Box { int x0; int y0; int x1; int y1; };
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 6;
}

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 34; bb.y0 = 26; bb.x1 = 58; bb.y1 = 98;
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
        acc = acc + rec1(240);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 92) % 3571;
        int c1 = (x * 92) % 3571;
        int c2 = (x * 92) % 3571;
        int c3 = (x * 92) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
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
            acc = acc + i * 20 + 21 * 26;
        } else {
            acc = acc + i * 22 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(366666);
    s = s + part1(4000);
    s = s + part2(500000);
    s = s + part3(666666);
    return ((s % 251) + 251) % 251;
}
