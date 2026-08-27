// Bounding-box updates; the box corners feed an invariant area term.
struct Box { int x0; int y0; int x1; int y1; };
int main() {
    struct Box bb;
    bb.x0 = 3;
    bb.y0 = 5;
    bb.x1 = 97;
    bb.y1 = 61;
    int acc = 0;
    int i = 0;
    while (i < 30000000) {
        int w = bb.x1 - bb.x0;
        int h = bb.y1 - bb.y0;
        acc = acc + w * h + w * w + h * h;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
