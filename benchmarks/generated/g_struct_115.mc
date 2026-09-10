// generated: single pattern 'struct'
struct __Box { int x0; int y0; int x1; int y1; };
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        struct __Box bb;
        bb.x0 = 19; bb.y0 = 5; bb.x1 = 67; bb.y1 = 56;
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h + w * h * i;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(5500000);
    return ((s % 251) + 251) % 251;
}
