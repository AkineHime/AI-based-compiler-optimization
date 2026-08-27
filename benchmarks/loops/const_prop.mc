// Constants flow through several assignments before use -> constant propagation.
int main() {
    int a = 5;
    int b = a + 3;
    int c = b * a;
    int d = c - b + a;
    int acc = 0;
    int i = 0;
    while (i < 45000000) {
        acc = acc + a * b + c * d + b * d;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
