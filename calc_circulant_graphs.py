maxn = 40
total = 0
for n in range(5, maxn + 1):
    with open(f"data/parsed/circ{n}", "r") as f:
        l = f.readline()
        total += int(l)

print(total)

