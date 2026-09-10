// generated: composite div+unroll+cse+licm

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 93713;
        int v = 46822;
        acc = acc + 137597286 / u + 721995362 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + i * 6 - (i - (i / 9) * 4);
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 22) % 10007;
        int c1 = (x * 22) % 10007;
        int c2 = (x * 22) % 10007;
        int c3 = (x * 22) % 10007;
        int c4 = (x * 22) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 180 * 178 * 87 + 178 * 87 + 180 * 180;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(800000);
    s = s + part2(1000000);
    s = s + part3(5200000);
    return ((s % 251) + 251) % 251;
}
