// (x*7919) % 10007 recomputed four times per iteration -> CSE removes three.
int main() {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < 14000000) {
        int u = (x * 7919) % 10007;
        int v = (x * 7919) % 10007;
        int w = (x * 7919) % 10007;
        int z = (x * 7919) % 10007;
        acc = acc + u + v + w + z;
        x = x + 3;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
