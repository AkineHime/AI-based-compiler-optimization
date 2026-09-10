// generated: composite cse+nested

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 47) % 6997;
        int c1 = (x * 47) % 6997;
        int c2 = (x * 47) % 6997;
        int c3 = (x * 47) % 6997;
        int c4 = (x * 47) % 6997;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 6) {
            inner = inner + j * 28 + i * 14;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1000000);
    s = s + part1(371428);
    return ((s % 251) + 251) % 251;
}
