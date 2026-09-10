// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 32 * 32 + 108 * 32 * 96 + 96 * 108 * 32 + 32 * 96 + 96 * 32 + 96 * 96;
    }
    return acc;
}

int main() {
    int s = part0(8000000);
    return ((s % 251) + 251) % 251;
}
