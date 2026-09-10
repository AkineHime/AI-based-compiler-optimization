// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 78246;
        int v = 59736;
        acc = acc + 1365064594 / u + 387175923 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(3600000);
    return ((s % 251) + 251) % 251;
}
