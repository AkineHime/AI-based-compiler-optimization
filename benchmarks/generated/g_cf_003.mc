// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 39;
        int q = 40;
        int r = 28;
        acc = acc + p * q * r + q * p * q + q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
