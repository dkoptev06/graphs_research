#include <bits/stdc++.h>
#include <stdexcept>

using namespace std;

bool is_triangle(int a, int b, int c) {
    return a <= b + c && b <= a + c && c <= a + b;
}

int main() {
    int C;
    cin >> C;

    for (int d1 = 0; d1 <= C; d1++) {
        for (int d2 = 0; d2 <= C; d2++) {
            for (int a = 0; a <= d1 + d2; a++) {
                for (int b = 0; b <= d1 + d2; b++) {
                    for (int c = 0; c <= d1 + d2; c++) {
                        if (!is_triangle(a, b, c)) {
                            continue;
                        }
                        for (int a1 = 0; a1 <= d1 && a1 <= a; a1++) {
                            int a2 = a - a1;
                            if (a2 > d2) {
                                continue;
                            }
                            bool ok = false;
                            for (int x = 0; !ok && x <= d1 && x <= b; x++) {
                                for (int y = 0; !ok && y <= d1 && y <= c; y++) {
                                    if (b - x > d2 || c - y > d2) {
                                        continue;
                                    }
                                    if (!is_triangle(a1, x, y)) {
                                        continue;
                                    }
                                    if (!is_triangle(a2, b - x, c - y)) {
                                        continue;
                                    }
                                    ok = true;
                                }
                            }
                            if (!ok) {
                                cout << d1 << ' ' << d2 << endl;
                                cout << a << ' ' << b << ' ' << c << endl;
                                cout << a1 << endl;
                                throw std::logic_error("Fail");
                            }
                        }
                    }
                }
            }
        }
    }
    cout << "Success!" << '\n';
}