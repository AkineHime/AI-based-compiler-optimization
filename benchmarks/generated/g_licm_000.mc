// generated: single pattern 'licm'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 23 * 112 + 112 * 112 + 23 * 23;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(8000000);
    return ((s % 251) + 251) % 251;
}
