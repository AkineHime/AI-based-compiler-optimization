// Fixed complex-number multiply in a hot loop -> LICM + CSE.
struct C { int re; int im; };
int main() {
    struct C a;
    struct C b;
    a.re = 7;
    a.im = 3;
    b.re = 5;
    b.im = 11;
    int acc = 0;
    int i = 0;
    while (i < 25000000) {
        int re = a.re * b.re - a.im * b.im;
        int im = a.re * b.im + a.im * b.re;
        acc = acc + re * re + im * im + re * im;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
