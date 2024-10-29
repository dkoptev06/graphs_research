#include <bits/stdc++.h>
#include <chrono>
#include <climits>

using namespace std;

typedef unsigned long long ull;

const int N = 11;
const int M = N * (N - 1) / 2;
const int INF = 1'000'000'000;
const int BENCHMARK_TEST_COUNT = 1000;

int diameter_upper_bound;
vector<vector<vector<pair<int, int>>>> triangles(N, vector<vector<pair<int, int>>>(N));

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

    static void ProcessGraphBasic(const vector<vector<int>> &gr, bool ignore_output = false) {
        vector<vector<int>> dist = GraphProcessor::CalculateDistanceMatrix(gr);
        int diameter = 0;
        for (int v = 0; v < N; v++) {
            diameter = max(diameter, *max_element(dist[v].begin(), dist[v].end()));
        }
        if (diameter == INF) {
            return;
        }

        bool good_graph = true;
        for (int a = 0; a < N && good_graph; a++) {
            for (int b = a + 1; b < N && good_graph; b++) {
                int d0 = dist[a][b];
                for (int d1 = 0; d1 <= diameter && good_graph; d1++) {
                    for (int d2 = 0; d2 <= diameter && good_graph; d2++) {
                        if (!(d1 + d0 >= d2 && d2 + d0 >= d1 && d1 + d2 >= d0)) {
                            continue;
                        }
                        bool c_exists = false;
                        for (int c = 0; c < N && !c_exists; c++) {
                            c_exists |= (dist[a][c] == d1 && dist[b][c] == d2);
                        }
                        good_graph &= c_exists;
                    }
                }
            }
        }

        if (good_graph && !ignore_output) {
            for (int v = 0; v < N; v++) {
                for (int u : gr[v]) {
                    if (u > v) {
                        cout << v + 1 << ' ' << u + 1 << '\n';
                    }
                }
            }
            cout << "\n---\n\n";
            cout.flush();
        }
    }

    static void ProcessGraphOptimized(const vector<vector<int>> &gr, bool ignore_output = false) {
        vector<vector<int>> dist = GraphProcessor::CalculateDistanceMatrix(gr);
        int diameter = 0;
        for (int v = 0; v < N; v++) {
            diameter = max(diameter, *max_element(dist[v].begin(), dist[v].end()));
        }
        if (diameter > diameter_upper_bound) {
            return;
        }

        bool good_graph = true;
        for (int a = 0; a < 1 && good_graph; a++) {
            for (int b = a + 1; b < N && good_graph; b++) {
                int d0 = dist[a][b];
                for (int d1 = 0; d1 <= diameter && good_graph; d1++) {
                    for (int d2 = 0; d2 <= diameter && good_graph; d2++) {
                        if (!(d1 + d0 >= d2 && d2 + d0 >= d1 && d1 + d2 >= d0)) {
                            continue;
                        }
                        bool c_exists = false;
                        for (int c = 0; c < N && !c_exists; c++) {
                            c_exists |= (dist[a][c] == d1 && dist[b][c] == d2);
                        }
                        good_graph &= c_exists;
                    }
                }
            }
        }

        for (int a = 1; a < N && good_graph; a++) {
            for (int b = a + 1; b < N && good_graph; b++) {
                int d0 = dist[a][b];
                vector<pair<int, int>> existing_triangles;
                existing_triangles.reserve(N);
                for (int c = 0; c < N; c++) {
                    existing_triangles.emplace_back(dist[a][c], dist[b][c]);
                }
                sort(existing_triangles.begin(), existing_triangles.end());
                vector<pair<int, int>> &expected_triangles = triangles[diameter][d0];
                for (int i = 0, j = 0; i < expected_triangles.size(); i++) {
                    while (j < existing_triangles.size() &&
                           existing_triangles[j] < expected_triangles[i]) {
                        j++;
                    }
                    if (j == existing_triangles.size() ||
                        existing_triangles[j] != expected_triangles[i]) {
                        good_graph = false;
                        break;
                    }
                }
            }
        }

        if (good_graph && !ignore_output) {
            for (int v = 0; v < N; v++) {
                for (int u : gr[v]) {
                    if (u > v) {
                        cout << v + 1 << ' ' << u + 1 << '\n';
                    }
                }
            }
            cout << "\n---\n\n";
            cout.flush();
        }
    }
};

void GenerateTriangles() {
    for (int diameter = 0; diameter < N; diameter++) {
        int max_triangle_count = 0;
        for (int d0 = 0; d0 <= diameter; d0++) {
            for (int d1 = 0; d1 <= diameter; d1++) {
                for (int d2 = 0; d2 <= diameter; d2++) {
                    if (!(d1 + d0 >= d2 && d2 + d0 >= d1 && d1 + d2 >= d0)) {
                        continue;
                    }
                    triangles[diameter][d0].emplace_back(d1, d2);
                }
            }
            sort(triangles[diameter][d0].begin(), triangles[diameter][d0].end());
            max_triangle_count = max(max_triangle_count, (int)triangles[diameter][d0].size());
        }
        if (N >= max_triangle_count) {
            diameter_upper_bound = diameter;
        }
    }
}

void Bruteforce() {
    assert(M < CHAR_BIT * sizeof(ull));
    for (ull mask = 0; mask < (1ll << M); mask++) {
        vector<vector<int>> gr(N);
        int ind = 0;
        for (int v = 0; v < N; v++) {
            for (int u = v + 1; u < N; u++) {
                if ((mask >> ind) & 1) {
                    gr[v].push_back(u);
                    gr[u].push_back(v);
                }
                ind++;
            }
        }
        GraphProcessor::ProcessGraphOptimized(gr);
    }
}

void ProcessNonIsomorphicGraphs() {
    std::ifstream file("data/parsed_graphs10c.txt");
    assert(file.is_open());
    int graph_count;
    file >> graph_count;
    for (int gr_id = 0; gr_id < graph_count; gr_id++) {
        int n, m;
        file >> n >> m;
        assert(n == 10);
        vector<vector<int>> gr(n);
        for (int i = 0; i < m; i++) {
            int v, u;
            file >> v >> u;
            assert((v >= 0 && v < n) && (u >= 0 && u < n));
            gr[v].push_back(u);
            gr[u].push_back(v);
        }
        GraphProcessor::ProcessGraphOptimized(gr);
    }
    cout << "Processed " << graph_count << " graphs\n";
}

mt19937 rng(179);

void BenchmarkGraphProcessing(int density, void processor(const vector<vector<int>> &, bool)) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    for (int t = 0; t < BENCHMARK_TEST_COUNT; t++) {
        vector<vector<int>> gr(N);
        for (int v = 0; v < N; v++) {
            for (int u = v + 1; u < N; u++) {
                if (rng() % density > 0) {
                    gr[v].push_back(u);
                    gr[u].push_back(v);
                }
            }
        }
        processor(gr, true);
    }

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    auto time = std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count();

    cout << "Benchmark with density = " << density << ": "
         << BENCHMARK_TEST_COUNT * 1000'000ll / time << " graphs per second" << endl;
}

void Benchmark() {
    cout << "Simple checker:" << endl;
    for (int density = 2; density <= 6; density += 2) {
        BenchmarkGraphProcessing(density, GraphProcessor::ProcessGraphBasic);
    }
    cout << "\n" << endl;
    cout << "Optimized checker:" << endl;
    for (int density = 2; density <= 6; density += 2) {
        BenchmarkGraphProcessing(density, GraphProcessor::ProcessGraphOptimized);
    }
}

int main(int argc, char *argv[]) {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);

    if (argc > 1) {
        freopen("output.txt", "w", stdout);
    }

    cout << "N = " << N << endl;
    {
        cout << "Generating triangles: " << endl;
        GenerateTriangles();
        cout << "Generating triangles finished" << endl;
    }

    cout << "Diameter upper bound: " << diameter_upper_bound << endl;

    {
        cout << "Running benchmark: " << endl;
        Benchmark();
        cout << "Benchmark finished" << endl;
    }

    // {
    //     cout << "Running bruteforce: " << endl;
    //     bruteforce();
    //     cout << "Bruteforce finished" << endl;
    // }

    // {
    //     cout << "Processing non-isomorphic graphs: " << endl;
    //     process_non_isomorphic_graphs();
    //     cout << "Processing non-isomorphic graphs finished" << endl;
    // }
}