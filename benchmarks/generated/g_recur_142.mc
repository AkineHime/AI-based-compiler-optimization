// generated: single pattern 'recur'
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 6;
}
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec0(160);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(10000);
    return ((s % 251) + 251) % 251;
}
