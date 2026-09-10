// generated: single pattern 'struct'
struct __Box { int x0; int y0; int x1; int y1; };
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        struct __Box bb;
        bb.x0 = 36; bb.y0 = 28; bb.x1 = 58; bb.y1 = 53;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
    }
    return acc;
}

int main() {
    int s = part0(12500000);
    return ((s % 251) + 251) % 251;
}
