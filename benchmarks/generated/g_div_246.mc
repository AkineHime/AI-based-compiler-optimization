// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 44321;
        int v = 97652;
        acc = acc + 1963569703 / u + 1723009216 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3600000);
    return ((s % 251) + 251) % 251;
}
