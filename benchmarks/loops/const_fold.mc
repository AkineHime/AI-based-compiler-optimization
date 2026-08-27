// Everything folds: single-assignment constants + a constant division.
int main() {
    int p = 17;
    int q = 23;
    int acc = 0;
    int i = 0;
    while (i < 14000000) {
        acc = acc + 2000000000 / p + 1999999997 / q + p * q * p + q * q * p;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
