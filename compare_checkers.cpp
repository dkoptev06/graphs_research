#include "dtg.cpp"

int main() {
    SimpleDtgChecker simple{};
    FastDtgChecker fast{};

    for (int n = 5; n <= 40; n += 5) {
        ull simple_count = simple.Benchmark(n);
        ull fast_count = fast.Benchmark(n);

        printf("n = %02d: Simple=%06llu, Fast=%06llu, Ratio=%04f\n", n, simple_count, fast_count,
               ((float)fast_count) / simple_count);
    }
}

/*
Output (on my machine):

n = 05: Simple=087634, Fast=198779, Ratio=2.268286
n = 10: Simple=037356, Fast=051129, Ratio=1.368696
n = 15: Simple=018603, Fast=022067, Ratio=1.186207
n = 20: Simple=009273, Fast=011492, Ratio=1.239297
n = 25: Simple=004789, Fast=006764, Ratio=1.412403
n = 30: Simple=002726, Fast=004298, Ratio=1.576669
n = 35: Simple=001760, Fast=002963, Ratio=1.683523
n = 40: Simple=001234, Fast=002009, Ratio=1.628039

*/