// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 189 * 189 + 183 * 189 + 183 * 189 * 187;
    }
    return acc;
}

int main() {
    int s = part0(25000000);
    return ((s % 251) + 251) % 251;
}
