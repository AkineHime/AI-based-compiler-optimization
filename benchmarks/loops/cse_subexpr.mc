// The compound expression (x*31 + 7) % 1009 recurs -> CSE computes it once.
int main() {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < 12000000) {
        int d = ((x * 31 + 7) % 1009) * ((x * 31 + 7) % 1009);
        int e = ((x * 31 + 7) % 1009) + ((x * 31 + 7) % 1009);
        acc = acc + d - e;
        x = x + 1;
        i = i + 1;
    }
    return ((acc % 251) + 251) % 251;
}
