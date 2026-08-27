int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}
int main() {
    int s = 0;
    int r = 0;
    while (r < 6) {
        s = s + fib(33);
        r = r + 1;
    }
    return ((s % 251) + 251) % 251;
}
