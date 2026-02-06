# graph_builder.py
import networkx as nx
import matplotlib.pyplot as plt
from logger_config import log

def build_dependency_graph(endpoints):
    G = nx.DiGraph()
    
    for path, methods in endpoints.items():
        if 'get' in methods:
            source_node = f"GET\n{path}"
            
            for other_path, other_methods in endpoints.items():
                for method in other_methods:
                    method = method.lower()
                    if method in ['put', 'delete', 'post']:
                        target_node = f"{method.upper()}\n{other_path}"
                        
                        if "{username}" in path and "{username}" in other_path:
                            if source_node != target_node:
                                G.add_edge(source_node, target_node)
    
    log.info(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def visualize_graph(G, filename="diploma_graph.png"):
    if G.number_of_nodes() == 0:
        log.warning("Graph is empty, nothing to draw.")
        return
    
    plt.figure(figsize=(14, 10), dpi=300)
    
    node_colors = []
    for node in G.nodes():
        if "GET" in node:
            node_colors.append('#90EE90')
        elif "DELETE" in node:
            node_colors.append('#FF7F7F')
        elif "PUT" in node:
            node_colors.append('#FFD700')
        else:
            node_colors.append('#ADD8E6')

    pos = nx.spring_layout(G, k=0.8, iterations=50)
    
    NODE_SIZE = 7000

    nx.draw_networkx_nodes(G, pos, node_size=NODE_SIZE, node_color=node_colors, edgecolors='grey', alpha=0.9)
    
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", font_family="sans-serif")
    
    nx.draw_networkx_edges(G, pos, 
                           node_size=NODE_SIZE, 
                           width=2, 
                           alpha=0.6, 
                           edge_color='gray', 
                           arrowstyle='-|>', 
                           arrowsize=25)
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    log.info(f"[+] Beautiful graph saved to {filename}")