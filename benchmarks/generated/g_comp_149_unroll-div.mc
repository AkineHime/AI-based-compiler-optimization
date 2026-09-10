// generated: composite unroll+div

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 5 - (i - (i / 3) * 3);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 40971;
        int v = 57585;
        acc = acc + 1930836153 / u + 379322782 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(550000);
    s = s + part1(300000);
    return ((s % 251) + 251) % 251;
}
