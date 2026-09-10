// generated: single pattern 'struct'
struct __Box { int x0; int y0; int x1; int y1; };
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 15; bb.y0 = 21; bb.x1 = 57; bb.y1 = 99;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3500000);
    return ((s % 251) + 251) % 251;
}
