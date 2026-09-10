// generated: single pattern 'cf'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int p = 23;
        int q = 8;
        int r = 20;
        acc = acc + r * r * p + p * p + p * q + (i - (i / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(7000000);
    return ((s % 251) + 251) % 251;
}
