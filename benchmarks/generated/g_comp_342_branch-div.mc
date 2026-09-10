// generated: composite branch+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 3 + 18 * 23;
        } else {
            acc = acc + i * 35 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 83648;
        int v = 59598;
        acc = acc + 129508647 / u + 1409016329 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
