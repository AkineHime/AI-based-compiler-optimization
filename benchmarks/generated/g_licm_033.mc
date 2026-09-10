// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 188 * 188 + 52 * 52 + 133 * 133;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(11000000);
    return ((s % 251) + 251) % 251;
}
