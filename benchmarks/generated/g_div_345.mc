// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 65017;
        int v = 53135;
        acc = acc + 1791551754 / u + 1711008182 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(6250000);
    return ((s % 251) + 251) % 251;
}
