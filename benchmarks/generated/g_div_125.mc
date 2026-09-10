// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 89758;
        int v = 69488;
        acc = acc + 1017883965 / u + 399780265 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2400000);
    return ((s % 251) + 251) % 251;
}
