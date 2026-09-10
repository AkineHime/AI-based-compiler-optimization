// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 75 * 75 + 75 * 199 + 199 * 132 * 75;
    }
    return acc;
}

int main() {
    int s = part0(18000000);
    return ((s % 251) + 251) % 251;
}
