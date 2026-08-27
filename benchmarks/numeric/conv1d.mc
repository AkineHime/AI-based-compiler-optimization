// 1-D convolution with a fixed 5-tap kernel, many passes.
int main() {
    int u[600];
    int w[600];
    int i = 0;
    while (i < 600) { u[i] = (i * 13) - ((i * 13) / 41) * 41; w[i] = 0; i = i + 1; }
    int k0 = 1;
    int k1 = 4;
    int k2 = 6;
    int k3 = 4;
    int k4 = 1;
    int rep = 0;
    while (rep < 40000) {
        i = 2;
        while (i < 598) {
            w[i] = u[i - 2] * k0 + u[i - 1] * k1 + u[i] * k2 + u[i + 1] * k3 + u[i + 2] * k4;
            i = i + 1;
        }
        i = 2;
        while (i < 598) { u[i] = w[i] - (w[i] / 251) * 251; i = i + 1; }
        rep = rep + 1;
    }
    int checksum = 0;
    i = 0;
    while (i < 600) { checksum = checksum + u[i]; i = i + 1; }
    return ((checksum % 251) + 251) % 251;
}
