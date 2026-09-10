// generated: composite licm+cse+div

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 197 * 197 + 60 * 60 + 197 * 60 * 158 + 60 * 158 * 197;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 88) % 4093;
        int c1 = (x * 88) % 4093;
        int c2 = (x * 88) % 4093;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 59883;
        int v = 56497;
        acc = acc + 1732301197 / u + 1205940642 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(300000);
    s = s + part1(300000);
    s = s + part2(400000);
    return ((s % 251) + 251) % 251;
}
