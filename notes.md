Написал самый простой перебор на C++ в файле [basic_bruteforce.cpp](./basic_bruteforce.cpp).

Компилировал следующей строкой:
`g++ basic_bruteforce.cpp -std=c++20 -O3 -DFILE_OUTPUT -o out/basic_bruteforce`

Время работы для разных $N$:
|$N$ | time |
|---|---|
|6|0.065s|
|7|4.8s|
|8|6m 27s|

```
dima@zenbook:~/Desktop/term_project$ time ~/nauty2_8_9/callgeng2 -c 11 > out/tmp.g6
>Z 1006700565 graphs made in 2014.65 seconds.

real    4m28.322s
user    12m48.475s
sys     20m46.427s
dima@zenbook:~/Desktop/term_project$ rm out/tmp.g6
dima@zenbook:~/Desktop/term_project$ time ~/nauty2_8_9/geng -c 11 > out/tmp.g6
>A /home/dima/nauty2_8_9/geng -cd1D10 n=11 e=10-55
>Z 1006700565 graphs generated in 284.22 sec

real    4m44.461s
user    4m31.432s
sys     0m12.790s
dima@zenbook:~/Desktop/term_project$ time ~/nauty2_8_9/geng -c -u 11
>A /home/dima/nauty2_8_9/geng -cd1D10 n=11 e=10-55
>Z 1006700565 graphs generated in 179.34 sec

real    2m59.346s
user    2m59.338s
sys     0m0.001s
dima@zenbook:~/Desktop/term_project$ time ~/nauty2_8_9/callgeng2 -u -c 11
>Z 1006700565 graphs made in 278.59 seconds.

real    0m33.324s
user    4m38.582s
sys     0m0.012s
dima@zenbook:~/Desktop/term_project$ 
```


compiling `geng`:
`gcc -o geng -O4  -mpopcnt -march=native -DMAXN=WORDSIZE -DWORDSIZE=32 geng.c gtoolsW.o nautyW1.o \
        nautilW1.o naugraphW1.o schreier.o naurng.o `



## inplace generation
```
dima@zenbook:~/nauty2_8_9$ ./aa_geng -c 9 > aa_output9.txt
>A ./aa_geng -cd1D8 n=9 e=8-36
>Z 261080 graphs generated in 0.48 sec
dima@zenbook:~/nauty2_8_9$ ./aa_geng -c 10 > aa_output10.txt
>A ./aa_geng -cd1D9 n=10 e=9-45
>Z 11716571 graphs generated in 24.06 sec
dima@zenbook:~/nauty2_8_9$ ./aa_geng -c 11 > aa_output11.txt
>A ./aa_geng -cd1D10 n=11 e=10-55
>Z 1006700565 graphs generated in 2362.41 sec
```

Compiling processing program: `g++ aa_outproc.cpp -c -o aa_outproc.o -O4 -mpopcnt -march=native -DMAXN=WORDSIZE -DOUTPROC=procname -DWORDSIZE=32` \
Compiling geng program: `gcc -o aa_geng.o -O4 -mpopcnt -march=native -DMAXN=WORDSIZE -DOUTPROC=procname -DWORDSIZE=32 -c geng.c` \
Linking: `g++ -o aa_geng aa_geng.o aa_outproc.o gtoolsW.o nautyW1.o nautilW1.o naugraphW1.o schreier.o naurng.o` \