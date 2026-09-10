// generated: single pattern 'unroll'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 7 - (i - (i / 6) * 8);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2500000);
    return ((s % 251) + 251) % 251;
}
