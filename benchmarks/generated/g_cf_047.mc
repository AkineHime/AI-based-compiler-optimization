// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 36;
        int q = 11;
        int r = 30;
        acc = acc + q * p * q + p * q * r + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(1666666);
    return ((s % 251) + 251) % 251;
}
