// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 66441;
        int v = 50566;
        acc = acc + 1467027483 / u + 697426024 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(2000000);
    return ((s % 251) + 251) % 251;
}
