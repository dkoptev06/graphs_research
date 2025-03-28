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

n = 05: Simple=272791, Fast=478720, Ratio=1.754897
n = 10: Simple=067498, Fast=100697, Ratio=1.491852
n = 15: Simple=025576, Fast=050845, Ratio=1.987997
n = 20: Simple=010426, Fast=038858, Ratio=3.727029
n = 25: Simple=004128, Fast=038257, Ratio=9.267684
n = 30: Simple=002049, Fast=041429, Ratio=20.219131
n = 35: Simple=001334, Fast=039457, Ratio=29.577961
n = 40: Simple=000913, Fast=035945, Ratio=39.370209

*/