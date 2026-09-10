// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 35;
        int q = 34;
        int r = 38;
        acc = acc + p * q * r + q * r + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(6000000);
    return ((s % 251) + 251) % 251;
}
