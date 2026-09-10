// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 66 * 113 + 66 * 66 + 66 * 21 + 113 * 66;
    }
    return acc;
}

int main() {
    int s = part0(12000000);
    return ((s % 251) + 251) % 251;
}
