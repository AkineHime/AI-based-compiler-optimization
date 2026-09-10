// generated: composite nested+cse

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 16) {
            inner = inner + j * 11 + i * 8;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 64) % 7919;
        int c1 = (x * 64) % 7919;
        int c2 = (x * 64) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(60000);
    s = s + part1(400000);
    return ((s % 251) + 251) % 251;
}
