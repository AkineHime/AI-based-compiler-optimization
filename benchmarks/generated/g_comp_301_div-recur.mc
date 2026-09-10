// generated: composite div+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 3;
}

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 92638;
        int v = 70335;
        acc = acc + 1112706279 / u + 680191010 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + rec1(120);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(6000);
    return ((s % 251) + 251) % 251;
}
