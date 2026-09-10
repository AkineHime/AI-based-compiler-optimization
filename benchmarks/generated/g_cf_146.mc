// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 19;
        int q = 21;
        int r = 9;
        acc = acc + q * p * q + p * q + p * q * r + r * r * p + p * p + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
