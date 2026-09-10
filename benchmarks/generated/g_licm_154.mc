// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 31 * 31 + 31 * 82 + 31 * 31 + 31 * 31 + 82 * 82;
    }
    return acc;
}

int main() {
    int s = part0(7000000);
    return ((s % 251) + 251) % 251;
}
