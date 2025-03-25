#include "dtg.cpp"

mt19937 rng(time(0));

FastDtgChecker checker{};

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
                dtg_count += checker.ProcessGraph(gr);
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
                    dtg_count += checker.ProcessGraph(gr);
                }
            });
        }
        for (int t = 0; t < thread_count; t++) {
            threads[t].join();
        }
        printf("%d: %d\n", n, dtg_count.load());
    }
}