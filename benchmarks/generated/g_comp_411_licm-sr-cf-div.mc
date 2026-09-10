// generated: composite licm+sr+cf+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 102 * 42 + 102 * 102 + 65 * 65 + 65 * 102 * 42 + 42 * 42;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 + i * 31 + i * 23 + 9;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int p = 13;
        int q = 16;
        int r = 23;
        acc = acc + q * p * q + q * r + r * r * p + (i - (i / 7) * 7);
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 87246;
        int v = 52849;
        acc = acc + 817277513 / u + 1418766741 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(2000000);
    s = s + part1(300000);
    s = s + part2(300000);
    s = s + part3(300000);
    return ((s % 251) + 251) % 251;
}
