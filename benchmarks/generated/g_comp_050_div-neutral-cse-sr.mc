// generated: composite div+neutral+cse+sr

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int u = 70714;
        int v = 77302;
        acc = acc + 879484715 / u + 721708857 / v + i / (u - (u / 100) * 100 + 1);
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 18) % 7919;
        int c1 = (x * 18) % 7919;
        int c2 = (x * 18) % 7919;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int part3(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + i * 5 + i * 17 + 5;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(400000);
    s = s + part1(5200000);
    s = s + part2(1000000);
    s = s + part3(400000);
    return ((s % 251) + 251) % 251;
}
