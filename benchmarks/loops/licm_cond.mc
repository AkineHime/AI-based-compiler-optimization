// Loop-invariant value used inside a branch -> LICM hoists it above the loop.
int main() {
    int a = 71;
    int b = 29;
    int acc = 0;
    int i = 0;
    while (i < 40000000) {
        int inv = a * b + a * a + b * b;
        if (i - (i / 2) * 2 == 0) {
            acc = acc + inv;
        } else {
            acc = acc - inv + a * b;
        }
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
