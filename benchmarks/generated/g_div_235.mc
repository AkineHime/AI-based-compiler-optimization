// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 46899;
        int v = 57132;
        acc = acc + 598853338 / u + 1483021894 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(4250000);
    return ((s % 251) + 251) % 251;
}
