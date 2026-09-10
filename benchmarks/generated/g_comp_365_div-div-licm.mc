// generated: composite div+div+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 70397;
        int v = 44517;
        acc = acc + 594693210 / u + 934501105 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 69487;
        int v = 50233;
        acc = acc + 651093249 / u + 1774052250 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 74 * 140 * 46 + 140 * 46 + 46 * 74 + 46 * 46;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(3000000);
    return ((s % 251) + 251) % 251;
}
