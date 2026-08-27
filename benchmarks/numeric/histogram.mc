// Bucket a stream into a fixed histogram, then reduce -> mostly array traffic.
int main() {
    int h[64];
    int i = 0;
    while (i < 64) { h[i] = 0; i = i + 1; }
    int x = 12345;
    int n = 0;
    while (n < 12000000) {
        x = (x * 1103515245 + 12345);
        int bucket = x - (x / 64) * 64;
        if (bucket < 0) { bucket = bucket + 64; }
        h[bucket] = h[bucket] + 1;
        n = n + 1;
    }
    int acc = 0;
    i = 0;
    while (i < 64) { acc = acc + h[i] * i; i = i + 1; }
    return ((acc % 251) + 251) % 251;
}
