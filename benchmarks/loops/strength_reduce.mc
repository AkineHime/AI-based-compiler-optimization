// acc += i * K in a hot loop -> strength reduction turns the multiply into an add.
int main() {
    int acc = 0;
    int i = 0;
    while (i < 45000000) {
        acc = acc + i * 13 + i * 31 + i * 57;
        i = i + 1;
    }
    return ((acc % 239) + 239) % 239;
}
