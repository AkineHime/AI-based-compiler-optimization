// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 62597;
        int v = 53338;
        acc = acc + 1505655080 / u + 1156976364 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2750000);
    return ((s % 251) + 251) % 251;
}
