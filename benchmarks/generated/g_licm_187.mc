// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 115 * 181 + 115 * 83 + 115 * 115 + 181 * 181 + 115 * 83 * 181;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(12000000);
    return ((s % 251) + 251) % 251;
}
