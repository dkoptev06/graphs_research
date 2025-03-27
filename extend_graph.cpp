#include "dtg.cpp"

const int INF = 1'000'000'000;

std::mutex output_mutex;
FastDtgChecker checker{};

void try_extend(vector<vector<int>> g, unsigned offset, unsigned step) {
    int n = g.size();
    assert(n < CHAR_BIT * sizeof(int));
    for (unsigned mask = offset; mask < (1u << n); mask += step) {
        vector<int> neighbours;
        for (int i = 0; i < n; i++) {
            if (mask & (1u << i)) {
                neighbours.push_back(i);
                g[i].push_back(n);
            }
        }
        g.push_back(neighbours);
        if (checker.ProcessGraph(g)) {
            std::unique_lock lock{output_mutex};
            cout << "Solution found:\n";
            for (int u : neighbours) {
                cout << u + 1 << ' ';
            }
            cout << '\n';
            return;
        }
        for (int u : g.back()) {
            g[u].pop_back();
        }
        g.pop_back();
    }
    {
        std::unique_lock lock{output_mutex};
        cout << "No solution was found in thread " << offset << '\n';
    }
}

void extend_multithread(const vector<vector<int>> &gr, const std::string &name) {
    cout << "Attempting to extend " << name << ": \n\n";

    int thread_count = std::thread::hardware_concurrency();
    vector<std::thread> threads;
    for (int t = 0; t < thread_count; t++) {
        threads.emplace_back([=] { try_extend(gr, t, thread_count); });
    }
    for (auto &tr : threads) {
        tr.join();
    }
}

vector<vector<int>> graph_from_edge_list(const vector<pair<int, int>> &edges) {
    int n = 0;
    for (auto [u, v] : edges) {
        n = max({n, u + 1, v + 1});
    }
    vector<vector<int>> gr(n);
    for (auto [u, v] : edges) {
        assert(v != u);
        assert(v >= 0 && v < n);
        assert(u >= 0 && u < n);

        gr[u].push_back(v);
        gr[v].push_back(u);
    }
    return gr;
}

int main(int argc, char *argv[]) {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);

    vector<vector<int>> test = graph_from_edge_list({{0, 1}, {1, 2}, {0, 2}});

    vector<vector<int>> g1 = graph_from_edge_list({
        // cartesian cube of a triangle
        {0, 9},   {0, 18},  {0, 3},   {0, 6},   {0, 1},   {0, 2},   {1, 10},  {1, 19},  {1, 4},   {1, 7},   {1, 2},
        {2, 11},  {2, 20},  {2, 5},   {2, 8},   {3, 12},  {3, 21},  {3, 6},   {3, 4},   {3, 5},   {4, 13},  {4, 22},
        {4, 7},   {4, 5},   {5, 14},  {5, 23},  {5, 8},   {6, 15},  {6, 24},  {6, 7},   {6, 8},   {7, 16},  {7, 25},
        {7, 8},   {8, 17},  {8, 26},  {9, 18},  {9, 12},  {9, 15},  {9, 10},  {9, 11},  {10, 19}, {10, 13}, {10, 16},
        {10, 11}, {11, 20}, {11, 14}, {11, 17}, {12, 21}, {12, 15}, {12, 13}, {12, 14}, {13, 22}, {13, 16}, {13, 14},
        {14, 23}, {14, 17}, {15, 24}, {15, 16}, {15, 17}, {16, 25}, {16, 17}, {17, 26}, {18, 21}, {18, 24}, {18, 19},
        {18, 20}, {19, 22}, {19, 25}, {19, 20}, {20, 23}, {20, 26}, {21, 24}, {21, 22}, {21, 23}, {22, 25}, {22, 23},
        {23, 26}, {24, 25}, {24, 26}, {25, 26},
    });

    vector<vector<int>> g2 = graph_from_edge_list({
        // circulant with diameter = 3
        {0, 3},   {0, 13},  {0, 14},  {0, 16},  {0, 17},  {0, 27},  {1, 4},   {1, 14},  {1, 15},  {1, 17},
        {1, 18},  {1, 28},  {2, 5},   {2, 15},  {2, 16},  {2, 18},  {2, 19},  {2, 29},  {3, 6},   {3, 16},
        {3, 17},  {3, 19},  {3, 20},  {4, 7},   {4, 17},  {4, 18},  {4, 20},  {4, 21},  {5, 8},   {5, 18},
        {5, 19},  {5, 21},  {5, 22},  {6, 9},   {6, 19},  {6, 20},  {6, 22},  {6, 23},  {7, 10},  {7, 20},
        {7, 21},  {7, 23},  {7, 24},  {8, 11},  {8, 21},  {8, 22},  {8, 24},  {8, 25},  {9, 12},  {9, 22},
        {9, 23},  {9, 25},  {9, 26},  {10, 13}, {10, 23}, {10, 24}, {10, 26}, {10, 27}, {11, 14}, {11, 24},
        {11, 25}, {11, 27}, {11, 28}, {12, 15}, {12, 25}, {12, 26}, {12, 28}, {12, 29}, {13, 16}, {13, 26},
        {13, 27}, {13, 29}, {14, 17}, {14, 27}, {14, 28}, {15, 18}, {15, 28}, {15, 29}, {16, 19}, {16, 29},
        {17, 20}, {18, 21}, {19, 22}, {20, 23}, {21, 24}, {22, 25}, {23, 26}, {24, 27}, {25, 28}, {26, 29},
    });

    assert(checker.ProcessGraph(test));
    assert(checker.ProcessGraph(g1));
    assert(checker.ProcessGraph(g2));

    // extend_multithread(test, "test graph");
    extend_multithread(g1, "cube of triangle");
    extend_multithread(g2, "circulant graph");
}