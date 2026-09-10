// generated: single pattern 'branch'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 4) * 4 == 0) {
            acc = acc + i * 22 + 27 * 6;
        } else {
            acc = acc + i * 8 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int main() {
    int s = part0(2666666);
    return ((s % 251) + 251) % 251;
}
