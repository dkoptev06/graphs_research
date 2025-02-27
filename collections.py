import subprocess
import tarfile
import requests
import gzip
import shutil

connected_by_edges_count = [
    'https://users.cecs.anu.edu.au/~bdm/data/ge1c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge2c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge3c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge4c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge5c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge6c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge7c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge8c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge9c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge10c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge11c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge12c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge13c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge14c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/ge15c.g6',
    # 'https://users.cecs.anu.edu.au/~bdm/data/ge16c.g6',
    # 'https://users.cecs.anu.edu.au/~bdm/data/ge17c.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/ge18c.g6.gz',
]

euler_graph_list = [
    'https://users.cecs.anu.edu.au/~bdm/data/eul3c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul4c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul5c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul6c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul7c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul8c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul9c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul10c.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/eul11c.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/euler12_1.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/euler12_2.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/euler12_3.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/euler12_4.g6.gz',
]

chordal_graph_list = [
    'https://users.cecs.anu.edu.au/~bdm/data/chordal4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal10.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/chordal11.g6',
    #'https://users.cecs.anu.edu.au/~bdm/data/chordal12.g6.gz',
    #'https://users.cecs.anu.edu.au/~bdm/data/chordal13.g6.gz',
]

perfect_graph_list = [
    'https://users.cecs.anu.edu.au/~bdm/data/perfect5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/perfect6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/perfect7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/perfect8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/perfect9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/perfect10.g6',
    #'https://users.cecs.anu.edu.au/~bdm/data/perfect11.g6.gz',
]


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

hypo_hamiltonian_list = [
    "https://users.cecs.anu.edu.au/~bdm/data/hypo10.g6",
    "https://users.cecs.anu.edu.au/~bdm/data/hypo13.g6",
    "https://users.cecs.anu.edu.au/~bdm/data/hypo15.g6",
    "https://users.cecs.anu.edu.au/~bdm/data/hypo16.g6",
    "https://users.cecs.anu.edu.au/~bdm/data/hypo18some.g6",
    "https://users.cecs.anu.edu.au/~bdm/data/hypo22some.g6",
    "https://users.cecs.anu.edu.au/~bdm/data/hypo26some.g6"
]

planar_list = [
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.1.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.2.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.3.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.10.g6.gz',
    #'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.11a.g6.gz',
    #'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.11b.g6.gz',
]

self_complementary = [
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp12.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp13.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/selfcomp16.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp17a.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp17b.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp17c.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_a.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_b.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_c.g6.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_d.g6.gz',

]

highly_irregular_list = [
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular1.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular2.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular10.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular11.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular12.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular13.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular14.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular15.g6',
]

critical_graphs = [
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_4_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_5_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_6_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_6_6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_7_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_7_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_7_7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_10.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_11.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_4.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_5.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_6.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_10.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_12.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_4.g6.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_5.g6.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_6.g6.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_7.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_8.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_9.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_10.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_11.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_13.g6',
    'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_14_4.g6.gz',

]

circulant_graphs = [
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ5.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ6.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ7.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ8.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ9.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ10.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ11.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ12.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ13.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ14.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ15.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ16.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ17.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ18.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ19.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ20.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ21.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ22.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ23.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ24.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ25.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ26.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ27.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ28.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ29.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ30.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ31.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ32.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ33.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ34.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ35.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ36.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ37.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ38.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ39.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ40.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ41.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ42.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ43.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ44.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ45.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ46.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ47.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ48.tar.gz',
    'https://users.cecs.anu.edu.au/~bdm/data/circ49.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ50.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ51.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ52.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ53.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ54.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ55.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ56.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ57.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ58.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ59.tar.gz',
    #  'https://users.cecs.anu.edu.au/~bdm/data/circ60.tar.gz',
    #  'https://users.cecs.anu.edu.au/~bdm/data/circ61.tar.gz',
    #  'https://users.cecs.anu.edu.au/~bdm/data/circ62.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ63.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ64.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ65.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ66.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ67.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ68.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ69.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ70.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ71.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ72.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ73.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ74.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ75.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ76.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ77.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ78.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ79.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ80.tar.gz',
    # 'https://users.cecs.anu.edu.au/~bdm/data/circ81.tar.gz',

]


CIRC_COLLECTION_NAME = "Circulant"

collections_url_list = [
    # (connected_by_edges_count, "Connected _ By Edge Count"),
    # (euler_graph_list, "Euler"),
    # (chordal_graph_list, "Chordal"),
    # (perfect_graph_list, "Perfect"),
    # (SRG_list, "Strongly Regular"), # all are discrete-triangular
    # (hypo_hamiltonian_list, "Hypo Hamiltonian"), # empty
    # (planar_list, "Planar"),
    # (self_complementary, "Self Complementary"),
    #(highly_irregular_list, "Highly Irregular"), # empty
    # (critical_graphs, "Critical"),
]

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
    print(f"\n\n\n---\nProcessing {collection_name}\n---\n\n\n")
    #out_file_all = f"data/output/{make_name_valid(collection_name)}.txt"
    out_file_d4 = f"data/output/{make_name_valid(collection_name)}D4.txt"
    #subprocess.call(f'touch {out_file_all}', shell=True)
    #subprocess.call(f'rm {out_file_all}', shell=True)
    subprocess.call(f'touch {out_file_d4}', shell=True)
    subprocess.call(f'rm {out_file_d4}', shell=True)
    for name in name_list:
        print(f"Processing {name}")
        if collection_name != CIRC_COLLECTION_NAME:
            with open(f'data/showg/{name}', 'r') as f_read:
                with open(f'data/parsed/{name}', 'w+') as f_write:
                    lines = f_read.readlines()
                    graphs = ''.join(lines).split("Graph")[1:]
                    f_write.write(f"{len(graphs)}\n")
                    for graph_line in graphs:
                        desc_parts = graph_line.split('.')
                        assert len(desc_parts) == 2
                        f_write.write(desc_parts[1].strip() + '\n')
        # subprocess.call(f'out/check_graphs_all < data/parsed/{name} >> {out_file_all}', shell=True)
        subprocess.call(f'out/check_graphs_d4 < data/parsed/{name} >> {out_file_d4}', shell=True)
    # with open(out_file_all, "a") as f:
    #     f.write("end")
    with open(out_file_d4, "a") as f:
        f.write("end")


def process_collections():
    for (collection, name) in collections_name_list:
        process_graph_list(collection, name)

import os.path

def download_circulant_graphs():
    batch_size_limit = 1000000
    print(f"Downloading {CIRC_COLLECTION_NAME}:")
    name_list = []
    for url in circulant_graphs:
        name = url.split('/')[-1]
        if os.path.isfile(f'data/raw/{name}'):
            print(f"Already have url: {url}")
        else:
            print(f"Getting url: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error: Response status code {response.status_code}")
                continue
            with open(f'data/raw/{name}', 'wb+') as f:
                f.write(response.content)
        print("Processing")
        assert name.endswith(".tar.gz")
        assert name.startswith("circ")
        tar = tarfile.open(f"data/raw/{name}")
        name = name[:-7]
        batch_number = 1
        n = int(name[4:])
        graphs = []

        def dump_on_disk():
            nonlocal graphs, name, batch_number
            batch_name = f"{name}_batch{batch_number}"
            with open(f'data/parsed/{batch_name}', 'w') as f_write:
                f_write.write(f"{len(graphs)}\n")
                for nums in graphs:
                    f_write.write(f"{n} {len(nums)}\n")
                    for num in nums:
                        f_write.write(f"{num} ")
                    f_write.write("\n")
            print(f'saved {batch_name}')
            name_list.append(batch_name)
            graphs = []
            batch_number += 1

        for member in tar.getmembers():
            f = tar.extractfile(member)
            content = f.read().decode('ascii')
            for line in content.split('\n'):
                if len(line.strip()) == 0:
                    continue
                nums = list(map(int, line.split()))
                graphs.append(nums)
                if len(graphs) == batch_size_limit:
                    dump_on_disk()

        dump_on_disk()

    global collections_name_list
    collections_name_list.append((name_list, CIRC_COLLECTION_NAME))


#download_collections()
download_circulant_graphs()
process_collections()


print("Success")

"""

'https://users.cecs.anu.edu.au/~bdm/data/graph2.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph2c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph3.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph3c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph4c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph5c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph6c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph7c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph8c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph9c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/graph10.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/graph10c.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/graph11.is6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/ge1d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge2d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge3d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge4d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge5d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge6d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge7d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge8d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge9d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge10d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge11d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge12d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge13d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge14d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge15d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge16d1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge17d1.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/ge1c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge2c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge3c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge4c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge5c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge6c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge7c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge8c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge9c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge10c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge11c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge12c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge13c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge14c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge15c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge16c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/ge17c.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/ge18c.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/eul2.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul3.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul3c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul4c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul5c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul6c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul7c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul8c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul9c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul10c.g6',
'https://users.cecs.anu.edu.au/~bdm/data/eul11.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/eul11c.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/euler12_1.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/euler12_2.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/euler12_3.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/euler12_4.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/chordal4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal11.g6',
'https://users.cecs.anu.edu.au/~bdm/data/chordal12.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/chordal13.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/perfect5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/perfect6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/perfect7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/perfect8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/perfect9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/perfect10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/perfect11.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/sr25832.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr251256.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr261034.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr271015.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr281264.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr291467.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr351668.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr351899.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr361446.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr361566.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/sr361566rep.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr371889some.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr401224.g6',
'https://users.cecs.anu.edu.au/~bdm/data/sr65321516some.g6',

'https://users.cecs.anu.edu.au/~bdm/data/hypo10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/hypo13.g6',
'https://users.cecs.anu.edu.au/~bdm/data/hypo15.g6',
'https://users.cecs.anu.edu.au/~bdm/data/hypo16.g6',
'https://users.cecs.anu.edu.au/~bdm/data/hypo18some.g6',
'https://users.cecs.anu.edu.au/~bdm/data/hypo22some.g6',
'https://users.cecs.anu.edu.au/~bdm/data/hypo26some.g6',

'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.2.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.3.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.10.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.11a.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/planar_conn.11b.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/selfcomp4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp12.g6',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp13.g6',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp16.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp17a.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp17b.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp17c.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_a.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_b.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_c.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/selfcomp20some_d.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular1.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular2.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular11.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular12.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular13.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular14.g6',
'https://users.cecs.anu.edu.au/~bdm/data/highlyirregular15.g6',

'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_4_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_5_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_6_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_6_6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_7_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_7_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_7_7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_8_8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_9_9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_10_10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_11_11.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_4.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_5.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_6.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_12_12.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_4.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_5.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_6.g6.gz',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_7.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_8.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_9.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_10.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_11.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_13_13.g6',
'https://users.cecs.anu.edu.au/~bdm/data/crit/crit_14_4.g6.gz',

'https://users.cecs.anu.edu.au/~bdm/data/circ5.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ6.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ7.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ8.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ9.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ10.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ11.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ12.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ13.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ14.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ15.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ16.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ17.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ18.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ19.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ20.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ21.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ22.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ23.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ24.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ25.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ26.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ27.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ28.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ29.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ30.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ31.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ32.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ33.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ34.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ35.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ36.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ37.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ38.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ39.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ40.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ41.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ42.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ43.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ44.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ45.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ46.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ47.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ48.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ49.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ50.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ51.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ52.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ53.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ54.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ55.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ56.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ57.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ58.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ59.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ60.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ61.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ62.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ63.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ64.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ65.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ66.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ67.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ68.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ69.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ70.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ71.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ72.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ73.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ74.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ75.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ76.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ77.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ78.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ79.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ80.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ81.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ82.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ83.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ84.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ85.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ86.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ87.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ88.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ89.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ90.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ91.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ92.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ93.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ94.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ95.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ96.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ97.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ98.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ99.tar.gz',
'https://users.cecs.anu.edu.au/~bdm/data/circ100.tar.gz',

"""
