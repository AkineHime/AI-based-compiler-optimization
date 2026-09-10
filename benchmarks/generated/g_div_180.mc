// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 62917;
        int v = 54263;
        acc = acc + 180432958 / u + 891795595 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3600000);
    return ((s % 251) + 251) % 251;
}
