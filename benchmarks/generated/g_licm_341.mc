// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 90 * 120 + 160 * 160 + 90 * 160 * 120 + 160 * 120 * 90;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(5000000);
    return ((s % 251) + 251) % 251;
}
