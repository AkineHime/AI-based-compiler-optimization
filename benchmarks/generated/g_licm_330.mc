// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 131 * 131 + 42 * 44 * 131 + 44 * 131 * 42;
    }
    return acc;
}

int main() {
    int s = part0(3000000);
    return ((s % 251) + 251) % 251;
}
