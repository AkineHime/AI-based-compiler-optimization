// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 178 * 178 + 178 * 175 * 190 + 178 * 175 + 175 * 175;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(5000000);
    return ((s % 251) + 251) % 251;
}
