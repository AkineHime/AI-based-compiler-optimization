// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 98 * 98 + 137 * 98 * 145 + 145 * 137 + 145 * 137 * 98 + 137 * 137 + 145 * 98;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3000000);
    return ((s % 251) + 251) % 251;
}
