// generated: composite cse+recur
int rec1(int n) {
    if (n < 2) { return n; }
    return rec1(n - 1) + 7;
}

int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 60) % 6997;
        int c1 = (x * 60) % 6997;
        int c2 = (x * 60) % 6997;
        int c3 = (x * 60) % 6997;
        acc = acc + c0 + c1 + c2 + c3;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + rec1(460);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(6000);
    return ((s % 251) + 251) % 251;
}
