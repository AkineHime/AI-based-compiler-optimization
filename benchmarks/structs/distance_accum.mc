// a.x, dx, dx*dx are all loop-invariant -> LICM + CF collapse the body.
struct Pt { int x; int y; };
int main() {
    struct Pt a;
    struct Pt b;
    a.x = 33;
    a.y = 71;
    b.x = 9;
    b.y = 24;
    int acc = 0;
    int i = 0;
    while (i < 45000000) {
        int dx = a.x - b.x;
        int dy = a.y - b.y;
        acc = acc + dx * dx + dy * dy + dx * dy + dx * dx * dy;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
