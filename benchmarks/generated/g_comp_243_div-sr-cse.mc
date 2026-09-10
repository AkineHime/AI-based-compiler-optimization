// generated: composite div+sr+cse

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 77845;
        int v = 95101;
        acc = acc + 507924140 / u + 446285380 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 57 + i * 11 + i * 31 + 9;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 15) % 7919;
        int c1 = (x * 15) % 7919;
        int c2 = (x * 15) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(750000);
    s = s + part1(3000000);
    s = s + part2(1000000);
    return ((s % 251) + 251) % 251;
}
