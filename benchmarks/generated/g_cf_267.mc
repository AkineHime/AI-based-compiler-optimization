// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 9;
        int q = 13;
        int r = 9;
        acc = acc + p * q * r + r * r * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(6000000);
    return ((s % 251) + 251) % 251;
}
