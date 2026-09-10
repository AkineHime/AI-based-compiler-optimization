// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 176 * 138 + 138 * 138 + 183 * 176 * 138 + 183 * 183 + 138 * 176 + 138 * 183;
    }
    return acc;
}

int main() {
    int s = part0(3000000);
    return ((s % 251) + 251) % 251;
}
