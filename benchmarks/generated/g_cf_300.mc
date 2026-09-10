// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 10;
        int q = 38;
        int r = 10;
        acc = acc + p * q * r + r * r * p + q * r + p * q + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(11000000);
    return ((s % 251) + 251) % 251;
}
