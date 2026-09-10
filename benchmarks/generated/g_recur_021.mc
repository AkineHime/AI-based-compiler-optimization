// generated: single pattern 'recur'
int rec0(int n) {
    if (n < 2) { return n; }
    return rec0(n - 1) + 4;
}
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec0(320);
    }
    return acc;
}

int main() {
    int s = part0(96153);
    return ((s % 251) + 251) % 251;
}
