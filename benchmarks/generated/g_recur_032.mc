// generated: single pattern 'recur'
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 2;
}
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(60);
    }
    return acc;
}

int main() {
    int s = part0(10000);
    return ((s % 251) + 251) % 251;
}
