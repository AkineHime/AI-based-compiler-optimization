// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 35;
        int q = 19;
        int r = 39;
        acc = acc + p * q + r * r * p + q * r + (i - (i / 7) * 7);
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
