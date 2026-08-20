struct Point {
    int x;
    int y;
};

int matrixSum(int m[3][3]) {
    int total = 0;
    int i = 0;
    while (i < 3) {
        int j = 0;
        while (j < 3) {
            total = total + m[i][j];
            j = j + 1;
        }
        i = i + 1;
    }
    return total;
}

int distanceSquared(struct Point a, struct Point b) {
    int dx = a.x - b.x;
    int dy = a.y - b.y;
    return dx * dx + dy * dy;
}

int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    char label[6] = "grid1";
    struct Point p1;
    p1.x = 0;
    p1.y = 0;
    struct Point p2;
    p2.x = 3;
    p2.y = 4;
    int grid[3][3];
    grid[0][0] = 1; grid[0][1] = 0; grid[0][2] = 0;
    grid[1][0] = 0; grid[1][1] = 1; grid[1][2] = 0;
    grid[2][0] = 0; grid[2][1] = 0; grid[2][2] = 1;
    int d = distanceSquared(p1, p2);
    int s = matrixSum(grid);
    int f = fib(10);
    return d + s + f;
}
