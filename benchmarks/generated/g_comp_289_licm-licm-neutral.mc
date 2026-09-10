// generated: composite licm+licm+neutral

int part0(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 195 * 195 + 172 * 172 + 195 * 121 + 172 * 195 * 121 + 121 * 172 * 195;
        i = i + 1;
    }
    return acc;
}

int part1(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        acc = acc + 196 * 173 * 64 + 173 * 173 + 64 * 64 + 196 * 196 + 64 * 196;
        i = i + 1;
    }
    return acc;
}

int part2(int reps) {
    int acc = 0;
    int i = 0;
    while (i < reps) {
        int t = acc - (acc / 100003) * 100003;
        acc = acc + t * 3 + i - (t - (t / 7) * 7);
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = 0;
    s = s + part0(1100000);
    s = s + part1(300000);
    s = s + part2(1133333);
    return ((s % 251) + 251) % 251;
}
