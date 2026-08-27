// A long expression whose sub-terms repeat -> CSE.
int main() {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < 14000000) {
        int p = (x * 977) % 4093;
        int q = (x * 977) % 4093;
        acc = acc + p * q + p * q + p * q + p * p + q * q;
        x = x + 1;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
