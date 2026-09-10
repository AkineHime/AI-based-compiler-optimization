// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 5;
        int q = 23;
        int r = 4;
        acc = acc + p * q * r + p * p + p * q + q * p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(1666666);
    return ((s % 251) + 251) % 251;
}
