with open('output11.txt', 'r') as f:
    data = ''.join(f.readlines())
    graphs = data.split("---")[:-1]
    assert len(graphs) == 12079
    for g in graphs:
        v = list(map(int, g.split()))
        for i in range(0, len(v), 2):
            print(f"({v[i]}, {v[i+1]})", end="")
            if i + 2 < len(v):
                print(', ', end="")
        print('],')
