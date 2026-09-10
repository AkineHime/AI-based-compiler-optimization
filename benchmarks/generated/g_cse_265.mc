// generated: single pattern 'cse'
int part0(int reps) {
    int acc = 0;
    int x = 1;
    for (int i = 0; i < reps; i = i + 1) {
        int c0 = (x * 77) % 6997;
        int c1 = (x * 77) % 6997;
        int c2 = (x * 77) % 6997;
        acc = acc + c0 + c1 + c2;
        x = x + 3;
    }
    return acc;
}

int main() {
    int s = part0(1500000);
    return ((s % 251) + 251) % 251;
}
