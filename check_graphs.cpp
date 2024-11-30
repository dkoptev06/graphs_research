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

        if (good_graph) {
            for (int v = 0; v < n; v++) {
                for (int u : gr[v]) {
                    if (u > v) {
                        cout << v + 1 << ' ' << u + 1 << '\n';
                    }
                }
            }
            cout << "\n---\n\n";
            cout.flush();
            return true;
        }
        return false;
    }
};

int main(int argc, char *argv[]) {
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);

    int graph_count;
    cin >> graph_count;
    for (int gr_id = 0; gr_id < graph_count; gr_id++) {
        int n, m;
        cin >> n >> m;
        vector<vector<int>> gr(n);
        for (int i = 0; i < m; i++) {
            int v, u;
            cin >> v >> u;
            assert((v >= 0 && v < n) && (u >= 0 && u < n));
            gr[v].push_back(u);
            gr[u].push_back(v);
        }
        GraphProcessor::ProcessGraphBasic(gr);
    }
}