// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 93865;
        int v = 69205;
        acc = acc + 711164247 / u + 1638946473 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3600000);
    return ((s % 251) + 251) % 251;
}
