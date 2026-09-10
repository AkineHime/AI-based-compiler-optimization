// generated: composite unroll+cse+cse+cse

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 3 - (i - (i / 6) * 3);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 17) % 3571;
        int c1 = (x * 17) % 3571;
        int c2 = (x * 17) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 92) % 6997;
        int c1 = (x * 92) % 6997;
        int c2 = (x * 92) % 6997;
        int c3 = (x * 92) % 6997;
        int c4 = (x * 92) % 6997;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 85) % 3571;
        int c1 = (x * 85) % 3571;
        int c2 = (x * 85) % 3571;
        int c3 = (x * 85) % 3571;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(400000);
    s = s + part2(400000);
    s = s + part3(1000000);
    return ((s % 251) + 251) % 251;
}
