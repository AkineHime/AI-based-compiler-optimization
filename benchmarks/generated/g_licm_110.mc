// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 82 * 82 + 82 * 39 * 141 + 141 * 39 + 141 * 82 * 39 + 141 * 82;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(18000000);
    return ((s % 251) + 251) % 251;
}
