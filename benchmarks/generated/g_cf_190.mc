// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 11;
        int q = 3;
        int r = 6;
        acc = acc + r * r * p + q * p * q + p * p + q * r + p * q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(1666666);
    return ((s % 251) + 251) % 251;
}
