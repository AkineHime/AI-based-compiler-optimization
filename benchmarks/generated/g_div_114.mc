// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 65569;
        int v = 97014;
        acc = acc + 1365247239 / u + 264069244 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(1600000);
    return ((s % 251) + 251) % 251;
}
