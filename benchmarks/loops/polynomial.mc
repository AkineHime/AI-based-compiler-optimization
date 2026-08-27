// (xr + 5) and (xr + 5)*(xr + 5) recur -> CSE.
int main() {
    int acc = 0;
    int x = 0;
    while (x < 16000000) {
        int xr = x - (x / 101) * 101;
        int t = (xr + 5) * (xr + 5);
        int u = (xr + 5) * (xr + 5) * (xr + 5);
        int w = (xr + 5) * (xr + 5) + (xr + 5);
        acc = acc + t + u + w;
        x = x + 1;
    }
    return ((acc % 251) + 251) % 251;
}
