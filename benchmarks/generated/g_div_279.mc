// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 54279;
        int v = 50540;
        acc = acc + 1638062311 / u + 1778884887 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(1500000);
    return ((s % 251) + 251) % 251;
}
