import json
import networkx as nx

def build_and_query_graph():
    # 1. Load data from Experiment 1
    with open("experiments/01_triple_extraction/result.json", "r") as f:
        data = json.load(f)

    # 2. Create Directed Graph
    G = nx.MultiDiGraph()

    for triple in data["triples"]:
        G.add_edge(triple["head"], triple["tail"], 
                   relation=triple["relation"], 
                   category=triple["category"])

    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.\n")

    # 3. Symbolic Reasoning Task 1: Authority Search
    print("--- Reasoning Task 1: Mencari Otoritas ---")
    target_node = "Harta Pusako Tinggi"
    # Find nodes that have 'otoritas' relation to the target
    authorities = []
    for u, v, k, d in G.edges(data=True, keys=True):
        if v == target_node and d['category'] == 'otoritas':
            authorities.append(u)
    
    print(f"Pertanyaan: Siapa yang memiliki otoritas atas '{target_node}'?")
    print(f"Jawaban: {', '.join(authorities)}\n")

    # 4. Symbolic Reasoning Task 2: Conflict Context
    print("--- Reasoning Task 2: Konteks Konflik ---")
    conflicts = data.get("conflicts", [])
    for conflict in conflicts:
        print(f"Deteksi Konflik: {conflict['description']}")
        print(f"Entitas Terlibat: {', '.join(conflict['involved_entities'])}\n")

    # 5. Symbolic Reasoning Task 3: Path Traversal (Pusako Rendah to Inheritance)
    print("--- Reasoning Task 3: Path Traversal ---")
    start_node = "Harta Pusako Rendah"
    print(f"Menelusuri relasi untuk '{start_node}':")
    for u, v, d in G.out_edges(start_node, data=True):
        print(f"  [{d['relation']}] -> {v} ({d['category']})")

if __name__ == "__main__":
    build_and_query_graph()
