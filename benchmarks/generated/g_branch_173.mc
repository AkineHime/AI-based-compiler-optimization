// generated: single pattern 'branch'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 19 + 19 * 15;
        } else {
            acc = acc + i * 31 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = part0(25000000);
    return ((s % 251) + 251) % 251;
}
