// Sieve of Eratosthenes, repeated; p*p recomputed in the loop guard.
int main() {
    int N = 120000;
    int sieve[120000];
    int total = 0;
    int rep = 0;
    while (rep < 45) {
        int i = 0;
        while (i < N) { sieve[i] = 1; i = i + 1; }
        int p = 2;
        while (p * p < N) {
            if (sieve[p] == 1) {
                int m = p * p;
                while (m < N) { sieve[m] = 0; m = m + p; }
            }
            p = p + 1;
        }
        int count = 0;
        i = 2;
        while (i < N) { count = count + sieve[i]; i = i + 1; }
        total = total + count;
        rep = rep + 1;
    }
    return ((total % 251) + 251) % 251;
}
