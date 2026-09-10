// generated: composite licm+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 146 * 165 + 165 * 35 + 146 * 146 + 35 * 146 * 165;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 45 * 106 + 184 * 184 + 45 * 45 + 45 * 184 + 106 * 184 * 45 + 45 * 106 * 184;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(2000000);
    return ((s % 251) + 251) % 251;
}
