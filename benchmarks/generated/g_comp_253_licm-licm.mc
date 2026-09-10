// generated: composite licm+licm

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 174 * 174 + 31 * 31 + 67 * 31;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 117 * 117 + 85 * 117 * 46 + 117 * 46 + 46 * 46 + 46 * 85 + 46 * 117;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
