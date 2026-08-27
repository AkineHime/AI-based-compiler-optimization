// Expression invariant w.r.t. the inner loop -> hoisted to the inner preheader.
int main() {
    int a = 31;
    int b = 17;
    int acc = 0;
    int i = 0;
    while (i < 7000) {
        int j = 0;
        while (j < 9000) {
            acc = acc + 2000000000 / a + a * b + a * a + b * b + i * a + i * b;
            j = j + 1;
        }
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
