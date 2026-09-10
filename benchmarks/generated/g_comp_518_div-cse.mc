// generated: composite div+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int u = 68741;
        int v = 55771;
        acc = acc + 509031070 / u + 1044730251 / v + i / (u - (u / 100) * 100 + 1);
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 21) % 6997;
        int c1 = (x * 21) % 6997;
        int c2 = (x * 21) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
