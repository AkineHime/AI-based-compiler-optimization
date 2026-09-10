// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 3;
        int q = 33;
        int r = 6;
        acc = acc + p * p + p * q + p * q * r + r * r * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(4000000);
    return ((s % 251) + 251) % 251;
}
