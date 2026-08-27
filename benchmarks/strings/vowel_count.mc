// s[i] re-indexed several times per iteration -> load CSE.
int main() {
    char s[46] = "the quick brown fox jumps over a lazy dog now";
    int acc = 0;
    int rep = 0;
    while (rep < 1400000) {
        int i = 0;
        int hits = 0;
        while (i < 45) {
            if (s[i] == 97) { hits = hits + 1; }
            if (s[i] == 101) { hits = hits + 3; }
            if (s[i] == 111) { hits = hits + 5; }
            if (s[i] == 117) { hits = hits + 7; }
            i = i + 1;
        }
        acc = acc + hits;
        rep = rep + 1;
    }
    return ((acc % 251) + 251) % 251;
}
