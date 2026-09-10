// generated: composite sr+div+branch

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 57 + i * 31 + 9;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 84622;
        int v = 40703;
        acc = acc + 337059480 / u + 287698304 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 19 + 29 * 9;
        } else {
            acc = acc + i * 7 - (i - (i / 5) * 5);
        }
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(400000);
    s = s + part2(5200000);
    return ((s % 251) + 251) % 251;
}
