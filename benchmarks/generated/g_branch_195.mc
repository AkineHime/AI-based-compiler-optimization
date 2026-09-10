// generated: single pattern 'branch'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 5 + 33 * 23;
        } else {
            acc = acc + i * 6 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = part0(1666666);
    return ((s % 251) + 251) % 251;
}
