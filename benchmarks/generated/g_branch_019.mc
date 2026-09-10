// generated: single pattern 'branch'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 34 + 8 * 13;
        } else {
            acc = acc + i * 31 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = part0(7000000);
    return ((s % 251) + 251) % 251;
}
