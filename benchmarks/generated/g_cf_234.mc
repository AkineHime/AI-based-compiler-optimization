// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 27;
        int q = 30;
        int r = 32;
        acc = acc + p * p + r * r * p + q * p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(6000000);
    return ((s % 251) + 251) % 251;
}
