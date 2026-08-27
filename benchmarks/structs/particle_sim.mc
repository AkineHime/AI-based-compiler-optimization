// Array-of-structs update loop (nested aggregate l-values resist hoisting).
struct P { int x; int y; int vx; int vy; };
int main() {
    struct P ps[64];
    int i = 0;
    while (i < 64) {
        ps[i].x = i;
        ps[i].y = 64 - i;
        ps[i].vx = (i - (i / 3) * 3) + 1;
        ps[i].vy = (i - (i / 5) * 5) + 1;
        i = i + 1;
    }
    int t = 0;
    while (t < 160000) {
        i = 0;
        while (i < 64) {
            ps[i].x = ps[i].x + ps[i].vx;
            ps[i].y = ps[i].y + ps[i].vy;
            i = i + 1;
        }
        t = t + 1;
    }
    int checksum = 0;
    i = 0;
    while (i < 64) {
        checksum = checksum + ps[i].x + ps[i].y;
        i = i + 1;
    }
    return ((checksum % 251) + 251) % 251;
}
