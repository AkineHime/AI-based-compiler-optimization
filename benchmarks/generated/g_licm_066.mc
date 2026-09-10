// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 97 * 152 * 15 + 15 * 97 * 152 + 15 * 97 + 97 * 97 + 15 * 15 + 152 * 152;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(4000000);
    return ((s % 251) + 251) % 251;
}
