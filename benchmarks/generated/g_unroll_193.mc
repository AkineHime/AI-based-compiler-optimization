// generated: single pattern 'unroll'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 4 - (i - (i / 3) * 3);
    }
    return acc;
}

int main() {
    int s = part0(11000000);
    return ((s % 251) + 251) % 251;
}
