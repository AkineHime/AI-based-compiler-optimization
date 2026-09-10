// generated: single pattern 'cse'
int part0(int reps) {
    int acc = 0;
    int x = 1;
    int i = 0;
    while (i < reps) {
        int c0 = (x * 18) % 6997;
        int c1 = (x * 18) % 6997;
        int c2 = (x * 18) % 6997;
        int c3 = (x * 18) % 6997;
        int c4 = (x * 18) % 6997;
        acc = acc + c0 + c1 + c2 + c3 + c4;
        x = x + 3;
        i = i + 1;
    }
    return acc;
}

int main() {
    int s = part0(2333333);
    return ((s % 251) + 251) % 251;
}
