// 1-D 3-point stencil, many sweeps (array loads resist hoisting).
int main() {
    int u[512];
    int w[512];
    int i = 0;
    while (i < 512) { u[i] = (i * 7) - ((i * 7) / 31) * 31; w[i] = 0; i = i + 1; }
    int wa = 2;
    int wb = 5;
    int wc = 2;
    int rep = 0;
    while (rep < 60000) {
        i = 1;
        while (i < 511) {
            w[i] = u[i - 1] * wa + u[i] * wb + u[i + 1] * wc;
            i = i + 1;
        }
        i = 1;
        while (i < 511) { u[i] = w[i] - (w[i] / 997) * 997; i = i + 1; }
        rep = rep + 1;
    }
    int checksum = 0;
    i = 0;
    while (i < 512) { checksum = checksum + u[i]; i = i + 1; }
    return ((checksum % 251) + 251) % 251;
}
