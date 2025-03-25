#include <bits/stdc++.h>
#include <chrono>
#include <climits>

using namespace std;

typedef unsigned long long ull;

namespace GraphUtilities {

const int INF = 1'000'000'000;
static mt19937 rng(179);

vector<vector<int>> CalculateDistanceMatrix(const vector<vector<int>> &gr) {
    int n = gr.size();
    vector<vector<int>> dist(n, vector<int>(n));
    for (int start_v = 0; start_v < n; start_v++) {
        for (int u = 0; u < n; u++) {
            dist[start_v][u] = INF;
        }
        dist[start_v][start_v] = 0;

        queue<int> q;
        q.push(start_v);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : gr[v]) {
                if (dist[start_v][u] > dist[start_v][v] + 1) {
                    dist[start_v][u] = dist[start_v][v] + 1;
                    q.push(u);
                }
            }
        }
    }
    return dist;
}
};  // namespace GraphUtilities

class DtgCheckerInterface {
public:
    virtual bool CheckDtgProperty(const vector<vector<int>> &gr, const vector<vector<int>> &dist, int diameter) = 0;

    // returns true iff the given graph is discrete-triangular. If print_graph = true, then print graph if it's
    // discrete-triangular.
    bool ProcessGraph(const vector<vector<int>> &gr, bool print_graph = false) {
        int n = gr.size();
        auto dist = GraphUtilities::CalculateDistanceMatrix(gr);
        int diameter = 0;
        for (int v = 0; v < n; v++) {
            diameter = max(diameter, *max_element(dist[v].begin(), dist[v].end()));
        }
        if (diameter == GraphUtilities::INF) {
            return false;
        }
        bool result = CheckDtgProperty(gr, dist, diameter);

        if (result && print_graph) {
            for (int v = 0; v < n; v++) {
                for (int u : gr[v]) {
                    if (u > v) {
                        cout << v + 1 << ' ' << u + 1 << '\n';
                    }
                }
            }
            cout << "\n---\n\n";
            cout.flush();
        }

        return result;
    }

    ull Benchmark(int n) {  // return speed of graph processing (graphs per second) on random graphs G(n, 1/2)
        std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

        for (int t = 0; t < BENCHMARK_TEST_COUNT; t++) {
            vector<vector<int>> gr(n);
            for (int v = 0; v < n; v++) {
                for (int u = v + 1; u < n; u++) {
                    if (GraphUtilities::rng() & 1) {
                        gr[v].push_back(u);
                        gr[u].push_back(v);
                    }
                }
            }
            ProcessGraph(gr);
        }

        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
        auto time = std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count();

        return BENCHMARK_TEST_COUNT * 1000'000ull / time;
    }

private:
    const int BENCHMARK_TEST_COUNT = 10000;
};

class SimpleDtgChecker : public DtgCheckerInterface {
public:
    SimpleDtgChecker() = default;

    bool CheckDtgProperty(const vector<vector<int>> &gr, const vector<vector<int>> &dist, int diameter) {
        int n = gr.size();

        bool good_graph = true;
        for (int a = 0; a < n && good_graph; a++) {
            for (int b = a + 1; b < n && good_graph; b++) {
                int d0 = dist[a][b];
                for (int d1 = 0; d1 <= diameter && good_graph; d1++) {
                    for (int d2 = 0; d2 <= diameter && good_graph; d2++) {
                        if (!(d1 + d0 >= d2 && d2 + d0 >= d1 && d1 + d2 >= d0)) {
                            continue;
                        }
                        bool c_exists = false;
                        for (int c = 0; c < n && !c_exists; c++) {
                            c_exists |= (dist[a][c] == d1 && dist[b][c] == d2);
                        }
                        good_graph &= c_exists;
                    }
                }
            }
        }

        return good_graph;
    }
};

class FastDtgChecker : public DtgCheckerInterface {
public:
    bool CheckDtgProperty(const vector<vector<int>> &gr, const vector<vector<int>> &dist, int diameter) {
        int n = gr.size();
        bool is_dtg = true;

        if (diameter == 2 && n <= CHAR_BIT * sizeof(ull)) {
            vector<ull> mask(n);
            for (int v = 0; v < n; v++) {
                for (int u : gr[v]) {
                    mask[v] |= (1ull << u);
                }
            }

            ull full_mask = (1ull << n) - 1;
            for (int v = 0; is_dtg && v < n; v++) {
                for (int u = v + 1; is_dtg && u < n; u++) {
                    ull pair_mask = ((1ull << u) | (1ull << v));
                    bool sect = (mask[v] & mask[u]) > 0;
                    bool not_inside = (mask[v] | mask[u] | pair_mask) != (mask[v] | pair_mask) &&
                                      (mask[v] | mask[u] | pair_mask) != (mask[u] | pair_mask);
                    bool not_covering = (mask[v] | mask[u] | pair_mask) != full_mask;
                    is_dtg &= (sect && not_inside && not_covering);
                }
            }

            return is_dtg;
        }

        for (int a = 0; a < n && is_dtg; a++) {
            for (int b = a + 1; b < n && is_dtg; b++) {
                int d0 = dist[a][b];
                for (int d1 = 0; d1 <= diameter && is_dtg; d1++) {
                    for (int d2 = 0; d2 <= diameter && is_dtg; d2++) {
                        if (!(d1 + d0 >= d2 && d2 + d0 >= d1 && d1 + d2 >= d0)) {
                            continue;
                        }
                        bool c_exists = false;
                        for (int c = 0; c < n && !c_exists; c++) {
                            c_exists |= (dist[a][c] == d1 && dist[b][c] == d2);
                        }
                        is_dtg &= c_exists;
                    }
                }
            }
        }

        return is_dtg;
    }
};