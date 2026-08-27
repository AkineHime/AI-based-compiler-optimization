// Caesar shift of a fixed buffer; base/shift are single-assignment constants.
int main() {
    char msg[32] = "attackatdawnfromthenorthside";
    int base = 97;
    int shift = 3;
    int acc = 0;
    int rep = 0;
    while (rep < 1100000) {
        int i = 0;
        int local = 0;
        while (i < 27) {
            int c = msg[i] - base;
            int e = (c + shift) - ((c + shift) / 26) * 26 + base;
            local = local + e;
            i = i + 1;
        }
        acc = acc + local;
        rep = rep + 1;
    }
    return ((acc % 251) + 251) % 251;
}
