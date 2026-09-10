// generated: composite cse+nested

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 44) % 10007;
        int c1 = (x * 44) % 10007;
        int c2 = (x * 44) % 10007;
        int c3 = (x * 44) % 10007;
        int c4 = (x * 44) % 10007;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 16 + i * 12;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(60000);
    return ((s % 251) + 251) % 251;
}
