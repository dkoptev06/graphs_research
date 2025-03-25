#include "dtg.cpp"

int main(int argc, char *argv[]) {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);

    FastDtgChecker checker{};

    int graph_count;
    cin >> graph_count;
    for (int gr_id = 0; gr_id < graph_count; gr_id++) {
        int n, m;
        cin >> n >> m;
        vector<vector<int>> gr(n);

        for (int i = 0, u, v; i < m; i++) {
            cin >> u >> v;
            --u, --v;
            gr[u].push_back(v);
            gr[v].push_back(u);
        }

        checker.ProcessGraph(gr, true);
    }
}