// Loop body is entirely loop-invariant arithmetic -> LICM/CF collapse it to one add.
int main() {
    int a = 123;
    int b = 45;
    int c = 67;
    int acc = 0;
    int i = 0;
    while (i < 60000000) {
        acc = acc + a * b + c * a + a * a + b * b + c * c + a * b * c;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
