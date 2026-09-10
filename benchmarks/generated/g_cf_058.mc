// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 38;
        int q = 15;
        int r = 31;
        acc = acc + p * q + q * p * q + q * r + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
