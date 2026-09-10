// generated: single pattern 'sr'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 17 + i * 23 + 6;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(11000000);
    return ((s % 251) + 251) % 251;
}
