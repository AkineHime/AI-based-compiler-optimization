// Euclid's GCD run on a fixed pair, many times -> modulo-heavy, few opts.
int main() {
    int acc = 0;
    int rep = 0;
    while (rep < 1600000) {
        int a = 1071 + rep - (rep / 7) * 7;
        int b = 462;
        while (b != 0) {
            int t = b;
            b = a - (a / b) * b;
            a = t;
        }
        acc = acc + a;
        rep = rep + 1;
    }
    return ((acc % 251) + 251) % 251;
}
