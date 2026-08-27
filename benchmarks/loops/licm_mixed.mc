// Half the body is loop-invariant, half varies with i.
int main() {
    int a = 44;
    int b = 19;
    int acc = 0;
    int i = 0;
    while (i < 35000000) {
        int inv = a * b + a * a + b * b;
        acc = acc + inv + i * 3 + (i - (i / 5) * 5);
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
