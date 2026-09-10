// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 74 * 113 + 74 * 74 + 74 * 109 + 113 * 74 + 74 * 109 * 113 + 113 * 113;
    }
    return acc;
}

int main() {
    int s = part0(4000000);
    return ((s % 251) + 251) % 251;
}
