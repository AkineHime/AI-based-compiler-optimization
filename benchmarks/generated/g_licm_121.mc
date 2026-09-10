// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 175 * 175 + 135 * 175 + 84 * 84;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(25000000);
    return ((s % 251) + 251) % 251;
}
