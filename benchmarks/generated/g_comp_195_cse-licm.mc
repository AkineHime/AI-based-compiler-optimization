// generated: composite cse+licm

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 15) % 7919;
        int c1 = (x * 15) % 7919;
        int c2 = (x * 15) % 7919;
        int c3 = (x * 15) % 7919;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 39 * 39 + 52 * 39 + 52 * 52;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
