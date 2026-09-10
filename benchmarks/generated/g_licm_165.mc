// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 88 * 188 * 49 + 88 * 49 + 88 * 88 + 188 * 188;
    }
    return acc;
}

int main() {
    int s = part0(5000000);
    return ((s % 251) + 251) % 251;
}
