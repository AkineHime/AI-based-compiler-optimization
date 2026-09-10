// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 96260;
        int v = 48727;
        acc = acc + 721931211 / u + 1000094241 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(2000000);
    return ((s % 251) + 251) % 251;
}
