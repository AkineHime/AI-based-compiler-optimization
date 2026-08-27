int ack(int m, int n) {
    if (m == 0) {
        return n + 1;
    }
    if (n == 0) {
        return ack(m - 1, 1);
    }
    return ack(m - 1, ack(m, n - 1));
}
int main() {
    int s = 0;
    int r = 0;
    while (r < 7) {
        s = s + ack(3, 7);
        r = r + 1;
    }
    return ((s % 251) + 251) % 251;
}
