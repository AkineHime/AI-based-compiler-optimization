// generated: composite sr+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 + i * 7 + i * 23 + 7;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 75554;
        int v = 83188;
        acc = acc + 733999189 / u + 785481705 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(800000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
