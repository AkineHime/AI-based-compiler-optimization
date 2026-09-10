// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 99888;
        int v = 43579;
        acc = acc + 1168942364 / u + 1318712829 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(6250000);
    return ((s % 251) + 251) % 251;
}
