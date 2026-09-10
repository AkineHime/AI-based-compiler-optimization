// generated: composite branch+div+cse+nested

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        if (i - (i / 3) * 3 == 0) {
            acc = acc + i * 31 + 19 * 15;
        } else {
            acc = acc + i * 12 - (i - (i / 5) * 5);
        }
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 89992;
        int v = 79947;
        acc = acc + 693071192 / u + 876094188 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 79) % 3571;
        int c1 = (x * 79) % 3571;
        int c2 = (x * 79) % 3571;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int j = 0;
        int inner = 0;
        while (j < 10) {
            inner = inner + j * 10 + i * 30;
            j = j + 1;
        }
        acc = acc + inner;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(666666);
    s = s + part1(300000);
    s = s + part2(500000);
    s = s + part3(40000);
    return ((s % 251) + 251) % 251;
}
