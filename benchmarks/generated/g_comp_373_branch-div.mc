// generated: composite branch+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 2) * 2 == 0) {
            acc = acc + i * 34 + 32 * 8;
        } else {
            acc = acc + i * 21 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 48569;
        int v = 73426;
        acc = acc + 162511294 / u + 1243603892 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1600000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
