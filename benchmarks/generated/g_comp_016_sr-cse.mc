// generated: composite sr+cse

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 3 + i * 57 + i * 31 + 4;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 89) % 7919;
        int c1 = (x * 89) % 7919;
        int c2 = (x * 89) % 7919;
        int c3 = (x * 89) % 7919;
        int c4 = (x * 89) % 7919;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(850000);
    return ((s % 251) + 251) % 251;
}
