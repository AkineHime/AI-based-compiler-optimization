// generated: composite cse+licm

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 40) % 3571;
        int c1 = (x * 40) % 3571;
        int c2 = (x * 40) % 3571;
        int c3 = (x * 40) % 3571;
        int c4 = (x * 40) % 3571;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 167 * 127 + 127 * 115 + 127 * 167 + 127 * 115 * 167;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(800000);
    return ((s % 251) + 251) % 251;
}
