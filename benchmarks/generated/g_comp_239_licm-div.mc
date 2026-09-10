// generated: composite licm+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 34 * 34 + 180 * 180 + 34 * 180 * 152 + 152 * 152 + 34 * 152 + 152 * 34;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 94363;
        int v = 52891;
        acc = acc + 573423454 / u + 703797535 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(3000000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
