// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 35;
        int q = 18;
        int r = 23;
        acc = acc + p * q + q * p * q + q * r + p * p + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
