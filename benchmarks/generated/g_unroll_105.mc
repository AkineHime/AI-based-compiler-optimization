// generated: single pattern 'unroll'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 5) * 3);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
