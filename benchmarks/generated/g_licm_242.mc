// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 12 * 12 + 17 * 17 + 189 * 189 + 17 * 189 + 12 * 17 * 189 + 189 * 12 * 17;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(17000000);
    return ((s % 251) + 251) % 251;
}
