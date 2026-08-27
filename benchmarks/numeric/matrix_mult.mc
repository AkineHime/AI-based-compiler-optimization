// 32x32 integer matrix multiply, repeated (2-D indexing resists these passes).
int main() {
    int A[32][32];
    int B[32][32];
    int C[32][32];
    int i = 0;
    while (i < 32) {
        int j = 0;
        while (j < 32) {
            A[i][j] = (i + j) - ((i + j) / 7) * 7;
            B[i][j] = (i * j + 1) - ((i * j + 1) / 5) * 5;
            C[i][j] = 0;
            j = j + 1;
        }
        i = i + 1;
    }
    int checksum = 0;
    int rep = 0;
    while (rep < 240) {
        i = 0;
        while (i < 32) {
            int j = 0;
            while (j < 32) {
                int sum = 0;
                int k = 0;
                while (k < 32) {
                    sum = sum + A[i][k] * B[k][j];
                    k = k + 1;
                }
                C[i][j] = sum;
                j = j + 1;
            }
            i = i + 1;
        }
        checksum = checksum + C[rep - (rep / 32) * 32][rep - (rep / 32) * 32];
        rep = rep + 1;
    }
    return ((checksum % 251) + 251) % 251;
}
