// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 12;
        int q = 21;
        int r = 12;
        acc = acc + p * q + q * r + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(7000000);
    return ((s % 251) + 251) % 251;
}
