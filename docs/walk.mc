// The running example in docs/WALKTHROUGH.md.
// Small enough that every stage's output stays readable, but it still has a
// constant to fold (scale), a repeated subexpression (i * scale), and a
// loop-carried multiply for strength reduction.
int main() {
    int scale = 8;
    int total = 0;
    int i = 0;
    while (i < 1000) {
        total = total + i * scale + i * scale;
        i = i + 1;
    }
    return total % 256;
}
