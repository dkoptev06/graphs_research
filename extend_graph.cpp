#include <bits/stdc++.h>
#include <climits>

using namespace std;

typedef unsigned long long ull;

const int INF = 1'000'000'000;

class GraphProcessor {
public:
    static vector<vector<int>> CalculateDistanceMatrix(const vector<vector<int>> &gr) {
        int n = gr.size();
        vector<vector<int>> dist(n, vector<int>(n, INF));
        for (int start_v = 0; start_v < n; start_v++) {
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

    static bool ProcessGraphBasic(const vector<vector<int>> &gr) {
        int n = gr.size();
        vector<vector<int>> dist = GraphProcessor::CalculateDistanceMatrix(gr);
        int diameter = 0;
        for (int v = 0; v < n; v++) {
            diameter = max(diameter, *max_element(dist[v].begin(), dist[v].end()));
        }

        if (diameter == INF) {
            return false;
        }

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

std::mutex output_mutex;

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
        if (GraphProcessor::ProcessGraphBasic(g)) {
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
        {0, 1},   {0, 2},   {0, 3},   {0, 4},   {0, 5},   {0, 6},   {1, 16},  {1, 4},   {1, 5},   {1, 14},
        {1, 17},  {2, 24},  {2, 4},   {2, 29},  {2, 6},   {2, 15},  {3, 7},   {3, 26},  {3, 5},   {3, 6},
        {3, 11},  {4, 12},  {4, 14},  {4, 15},  {5, 7},   {5, 8},   {5, 17},  {6, 24},  {6, 26},  {6, 25},
        {7, 8},   {7, 9},   {7, 10},  {7, 11},  {8, 18},  {8, 10},  {8, 17},  {8, 19},  {9, 12},  {9, 28},
        {9, 10},  {9, 11},  {9, 15},  {10, 12}, {10, 13}, {10, 19}, {11, 26}, {11, 28}, {11, 27}, {12, 13},
        {12, 14}, {12, 15}, {13, 20}, {13, 14}, {13, 19}, {13, 21}, {14, 16}, {14, 21}, {15, 28}, {15, 29},
        {16, 22}, {16, 17}, {16, 21}, {16, 23}, {17, 18}, {17, 23}, {18, 24}, {18, 19}, {18, 23}, {18, 25},
        {19, 20}, {19, 25}, {20, 26}, {20, 21}, {20, 25}, {20, 27}, {21, 22}, {21, 27}, {22, 28}, {22, 23},
        {22, 27}, {22, 29}, {23, 24}, {23, 29}, {24, 25}, {24, 29}, {25, 26}, {26, 27}, {27, 28}, {28, 29},
    });

    assert(GraphProcessor::ProcessGraphBasic(test));
    assert(GraphProcessor::ProcessGraphBasic(g1));
    assert(GraphProcessor::ProcessGraphBasic(g2));

    // extend_multithread(test, "test graph");
    extend_multithread(g1, "cube of triangle");
    extend_multithread(g2, "circulant graph");
}