// generated: composite cse+div

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 39) % 10007;
        int c1 = (x * 39) % 10007;
        int c2 = (x * 39) % 10007;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 98707;
        int v = 58407;
        acc = acc + 752628083 / u + 523297160 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
