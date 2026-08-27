// Two loop-invariant integer divisions -> LICM hoists both out of the loop.
int main() {
    int a = 91127;
    int b = 71993;
    int acc = 0;
    int i = 0;
    while (i < 12000000) {
        acc = acc + 2000000000 / a + 1999999997 / b + 1000003 / a;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
