// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 25;
        int q = 37;
        int r = 8;
        acc = acc + p * q + q * p * q + p * q * r + q * r + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2666666);
    return ((s % 251) + 251) % 251;
}
