// generated: single pattern 'sr'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 13 + 5;
    }
    return acc;
}

int main() {
    int s = part0(18000000);
    return ((s % 251) + 251) % 251;
}
