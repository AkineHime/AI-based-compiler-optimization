// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 44745;
        int v = 57624;
        acc = acc + 136145850 / u + 1462448471 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(1500000);
    return ((s % 251) + 251) % 251;
}
