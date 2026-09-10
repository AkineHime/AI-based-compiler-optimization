// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 92647;
        int v = 44063;
        acc = acc + 651937565 / u + 518633576 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2000000);
    return ((s % 251) + 251) % 251;
}
