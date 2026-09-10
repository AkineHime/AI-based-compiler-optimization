// generated: single pattern 'unroll'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 - (i - (i / 5) * 3);
    }
    return acc;
}

int main() {
    int s = part0(2500000);
    return ((s % 251) + 251) % 251;
}
