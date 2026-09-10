// generated: single pattern 'cse'
int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 13) % 10007;
        int c1 = (x * 13) % 10007;
        int c2 = (x * 13) % 10007;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(3000000);
    return ((s % 251) + 251) % 251;
}
