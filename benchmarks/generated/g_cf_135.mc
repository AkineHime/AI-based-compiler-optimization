// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 3;
        int q = 11;
        int r = 17;
        acc = acc + p * p + q * r + q * p * q + p * q * r + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(7000000);
    return ((s % 251) + 251) % 251;
}
