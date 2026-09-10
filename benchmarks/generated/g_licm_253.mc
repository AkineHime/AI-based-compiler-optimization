// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 18 * 18 + 18 * 18 + 116 * 116 + 18 * 116 + 116 * 18 * 18 + 18 * 18;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(8000000);
    return ((s % 251) + 251) % 251;
}
