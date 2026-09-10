// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 15;
        int q = 18;
        int r = 28;
        acc = acc + p * p + p * q + p * q * r + q * r + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2666666);
    return ((s % 251) + 251) % 251;
}
