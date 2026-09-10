// generated: composite licm+neutral

int part0(int reps) {
    int acc = 0;
    for (int i = 0; i < reps; i = i + 1) {
        acc = acc + 172 * 184 + 184 * 184 + 172 * 172 + 184 * 172 + 172 * 193 + 172 * 193 * 184;
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

int main() {
    int s = 0;
    s = s + part0(600000);
    s = s + part1(366666);
    return ((s % 251) + 251) % 251;
}
