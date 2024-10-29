count = 0
n = int(input())
with open(f'data/raw_human_graphs{n}c.txt', 'r') as f_read:
    with open(f'data/parsed_graphs{n}c.txt', 'w') as f_write:
        lines = f_read.readlines()
        graphs = ''.join(lines).split("Graph")[1:]
        f_write.write(f"{len(graphs)}\n")
        for graph_line in graphs:
            desc_parts = graph_line.split('.')
            assert len(desc_parts) == 2
            f_write.write(desc_parts[1].strip() + '\n')

print(f"Success")
