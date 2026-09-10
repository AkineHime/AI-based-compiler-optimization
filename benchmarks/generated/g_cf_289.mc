// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 38;
        int q = 11;
        int r = 33;
        acc = acc + p * q + r * r * p + q * p * q + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(25000000);
    return ((s % 251) + 251) % 251;
}
