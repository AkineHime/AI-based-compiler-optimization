// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 53944;
        int v = 59199;
        acc = acc + 1176237035 / u + 616554406 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(2000000);
    return ((s % 251) + 251) % 251;
}
