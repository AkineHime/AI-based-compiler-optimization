// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 99 * 99 + 56 * 80 + 56 * 99;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(12000000);
    return ((s % 251) + 251) % 251;
}
