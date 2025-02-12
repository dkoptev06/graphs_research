#include <bits/stdc++.h>
#include <climits>

using namespace std;

mt19937 rng(time(0));

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

int main(int argc, char *argv[]) {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);

    if (argc < 4 || argc > 5) {
        cerr << "Usage: `{program_name} n_l n_r graph_count [thread_count]`. \n";
        return 1;
    }

    int n_l = stoi(argv[1]);
    int n_r = stoi(argv[2]);
    int graph_count = stoi(argv[3]);
    int thread_count = std::thread::hardware_concurrency();
    if (argc == 5) {
        thread_count = stoi(argv[4]);
    }

    vector<int> rng_seeds(thread_count);
    for (int t = 0; t < thread_count; t++) {
        rng_seeds[t] = rng();
    }

    for (int n = n_l; n <= n_r; n++) {
        std::atomic<int> graphs_processed = 0;
        std::atomic<int> dtg_count = 0;

        auto count_graphs = [&](int t_id) {
            mt19937 thread_rng(rng_seeds[t_id]);
            for (int gr_id = 0; gr_id < graph_count; gr_id++) {
                vector<vector<int>> gr(n);
                for (int v = 0; v < n; v++) {
                    for (int u = v + 1; u < n; u++) {
                        if (rng() & 1) {
                            gr[v].push_back(u);
                            gr[u].push_back(v);
                        }
                    }
                }
                dtg_count += GraphProcessor::ProcessGraphBasic(gr);
            }
        };

        vector<std::thread> threads;
        for (int t = 0; t < thread_count; t++) {
            threads.emplace_back([&, t]() {
                mt19937 thread_rng(rng_seeds[t]);
                while (1) {
                    if (graphs_processed.fetch_add(1) >= graph_count) {
                        return;
                    }
                    vector<vector<int>> gr(n);
                    for (int v = 0; v < n; v++) {
                        for (int u = v + 1; u < n; u++) {
                            if (thread_rng() & 1) {
                                gr[v].push_back(u);
                                gr[u].push_back(v);
                            }
                        }
                    }
                    dtg_count += GraphProcessor::ProcessGraphBasic(gr);
                }
            });
        }
        for (int t = 0; t < thread_count; t++) {
            threads[t].join();
        }
        printf("%d: %d\n", n, dtg_count.load());
    }
}