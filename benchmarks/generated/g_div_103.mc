// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 46522;
        int v = 85363;
        acc = acc + 567493145 / u + 1551071151 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(1600000);
    return ((s % 251) + 251) % 251;
}
