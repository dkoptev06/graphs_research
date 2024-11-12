import subprocess
import requests
import gzip
import shutil

SRG_list = ['https://users.cecs.anu.edu.au/~bdm/data/sr25832.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr251256.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr261034.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr271015.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr281264.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr291467.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr351668.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr351899.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr361446.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr361566.g6.gz',
            'https://users.cecs.anu.edu.au/~bdm/data/sr371889some.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr401224.g6',
            'https://users.cecs.anu.edu.au/~bdm/data/sr65321516some.g6']


collections_url_list = [(SRG_list, "Strongly Regular Graphs D3")]
collections_name_list = []


def download_from_url_list(url_list, collection_name):
    print(f"Downloading {collection_name}:")
    name_list = []
    for url in url_list:
        name = url.split('/')[-1]
        print(f"Getting url: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Response status code {response.status_code}")
            continue
        with open(f'data/raw/{name}', 'wb+') as f:
            f.write(response.content)
        if name.endswith(".gz"):
            name = name[:-3]
            with gzip.open(f'data/raw/{name}.gz', 'rb') as f_in:
                with open(f'data/raw/{name}', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        subprocess.call(f'~/nauty2_8_9/showg -e ./data/raw/{name} > ./data/showg/{name}', shell=True)
        name_list.append(name)

    global collections_name_list
    collections_name_list.append((name_list, collection_name))


def download_collections():
    for (collection, name) in collections_url_list:
        download_from_url_list(collection, name)

def make_name_valid(s):
    return "".join(x for x in s if x.isalnum())


def process_graph_list(name_list, collection_name):
    print(f"Processing {collection_name}")
    out_file = f"data/output/{make_name_valid(collection_name)}.txt"
    subprocess.call(f'rm {out_file}', shell=True)
    for name in name_list:
        with open(f'data/showg/{name}', 'r') as f_read:
            with open(f'data/parsed/{name}', 'w+') as f_write:
                lines = f_read.readlines()
                graphs = ''.join(lines).split("Graph")[1:]
                f_write.write(f"{len(graphs)}\n")
                for graph_line in graphs:
                    desc_parts = graph_line.split('.')
                    assert len(desc_parts) == 2
                    f_write.write(desc_parts[1].strip() + '\n')
        subprocess.call(f'out/check_graphs < data/parsed/{name} >> {out_file}', shell=True)
    with open(out_file, "a") as f:
        f.write("end")


def process_collections():
    for (collection, name) in collections_name_list:
        process_graph_list(collection, name)


download_collections()
process_collections()

print("Success")

# subprocess.call("./out/basic_bruteforce")

# response = requests.get("https://users.cecs.anu.edu.au/~bdm/data/graph9c.g6")
