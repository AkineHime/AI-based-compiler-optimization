// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 18;
        int q = 28;
        int r = 5;
        acc = acc + r * r * p + p * p + q * p * q + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
