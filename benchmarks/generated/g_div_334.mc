// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 50878;
        int v = 96424;
        acc = acc + 1892966809 / u + 1144382434 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(1600000);
    return ((s % 251) + 251) % 251;
}
