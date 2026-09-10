// generated: single pattern 'div'
int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 68974;
        int v = 60708;
        acc = acc + 255791554 / u + 1541295357 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = part0(4250000);
    return ((s % 251) + 251) % 251;
}
