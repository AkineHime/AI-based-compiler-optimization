int tak(int x, int y, int z) {
    if (y < x) {
        return tak(tak(x - 1, y, z), tak(y - 1, z, x), tak(z - 1, x, y));
    }
    return z;
}
int main() {
    int s = 0;
    int r = 0;
    while (r < 40) {
        s = s + tak(18, 12, 6);
        r = r + 1;
    }
    return ((s % 251) + 251) % 251;
}
