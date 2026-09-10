// generated: single pattern 'branch'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 19 + 3 * 6;
        } else {
            acc = acc + i * 38 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2666666);
    return ((s % 251) + 251) % 251;
}
