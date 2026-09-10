// generated: composite cse+unroll

int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 60) % 4093;
        int c1 = (x * 60) % 4093;
        int c2 = (x * 60) % 4093;
        int c3 = (x * 60) % 4093;
        int c4 = (x * 60) % 4093;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 8 - (i - (i / 4) * 3);
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(1600000);
    return ((s % 251) + 251) % 251;
}
