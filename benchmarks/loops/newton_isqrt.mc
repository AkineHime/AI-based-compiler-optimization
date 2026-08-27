// Integer square root by Newton iteration, repeated -> division-heavy.
int main() {
    int acc = 0;
    int n = 1000003;
    int rep = 0;
    while (rep < 900000) {
        int x = n;
        int y = (x + 1) / 2;
        int k = 0;
        while (y < x) {
            x = y;
            y = (x + n / x) / 2;
            k = k + 1;
            if (k > 40) { x = y; }
        }
        acc = acc + x;
        rep = rep + 1;
    }
    return ((acc % 251) + 251) % 251;
}
