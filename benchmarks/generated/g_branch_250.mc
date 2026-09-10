// generated: single pattern 'branch'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 16 + 21 * 23;
        } else {
            acc = acc + i * 24 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = part0(7000000);
    return ((s % 251) + 251) % 251;
}
