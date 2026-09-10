// generated: single pattern 'unroll'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 7 - (i - (i / 5) * 5);
    }
    return acc;
}

int main() {
    int s = part0(25000000);
    return ((s % 251) + 251) % 251;
}
