// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 88093;
        int v = 85944;
        acc = acc + 1844226845 / u + 1185641113 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3600000);
    return ((s % 251) + 251) % 251;
}
