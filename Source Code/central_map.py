"""
HAMP-IN Framework: Phase 1 (Global Offline Planning)
File: central_map.py
Description: Initializes the plant topology network, segregates spatial node structures 
             using K-Means clustering, resolves initial dual-Hamiltonian paths, 
             and provides a separate mathematical clustering diagram.
"""

import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def generate_centralized_baseline_map():
    """
    Initializes the industrial grid, clusters infrastructure nodes into distinct robot 
    territories via K-Means, and resolves the initial dual-Hamiltonian paths.
    """
    # Initialize topological graph structure
    G = nx.DiGraph()
    
    # 12-Node Industrial Facility Layout (0 to 100 Meter Scale Layout coordinates)
    nodes_data = {
        1:  {"name": "Intake",       "pos": (15, 75), "risk": 0.10},
        2:  {"name": "Storage",      "pos": (35, 75), "risk": 0.15},
        3:  {"name": "Compressor_1", "pos": (15, 45), "risk": 0.45},
        4:  {"name": "Boiler",       "pos": (50, 75), "risk": 0.60},
        5:  {"name": "Compressor_2", "pos": (15, 15), "risk": 0.45},
        6:  {"name": "Assembly",     "pos": (35, 15), "risk": 0.20},
        7:  {"name": "Pressing",     "pos": (60, 45), "risk": 0.35},
        8:  {"name": "Paint_Shop",   "pos": (70, 75), "risk": 0.90},  
        9:  {"name": "Oven_1",       "pos": (50, 45), "risk": 0.85},  
        10: {"name": "Oven_2",       "pos": (60, 15), "risk": 0.70},
        11: {"name": "Quality",      "pos": (85, 45), "risk": 0.10},
        12: {"name": "Output",       "pos": (90, 75), "risk": 0.05}
    }
    
    edges = [
        (1, 2, 0.015), (2, 4, 0.020), (4, 8, 0.025), (8, 12, 0.025),
        (1, 3, 0.015), (3, 5, 0.015), (5, 6, 0.015), (6, 10, 0.025),
        (10, 11, 0.025), (12, 11, 0.015), (1, 9, 0.025), (9, 4, 0.020),
        (4, 9, 0.015), (9, 7, 0.015), (7, 8, 0.025), (8, 11, 0.015),
        (3, 9, 0.015), (9, 10, 0.029), (7, 10, 0.009)
    ]
    
    for node, data in nodes_data.items():
        G.add_node(node, name=data["name"], pos=data["pos"], risk=data["risk"])
        
    for u, v, w in edges:
        G.add_edge(u, v, base_dist=w)

    # Node Segregation via Spatial K-Means Clustering
    node_ids = list(nodes_data.keys())
    coordinates = np.array([nodes_data[nid]["pos"] for nid in node_ids])
    
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    labels = kmeans.fit_predict(coordinates)
    centroids = kmeans.cluster_centers_
    
    cluster_1_nodes = [node_ids[i] for i in range(len(node_ids)) if labels[i] == 0]
    cluster_2_nodes = [node_ids[i] for i in range(len(node_ids)) if labels[i] == 1]

    def solve_hamiltonian_path(node_subset):
        if not node_subset:
            return []
        remaining = list(node_subset)
        current_node = min(remaining, key=lambda n: nodes_data[n]["pos"][0])
        path = [current_node]
        remaining.remove(current_node)
        
        while remaining:
            curr_pos = nodes_data[current_node]["pos"]
            next_node = min(remaining, key=lambda n: math.dist(curr_pos, nodes_data[n]["pos"]))
            path.append(next_node)
            remaining.remove(next_node)
            current_node = next_node
            
        return path

    r1_base_path = solve_hamiltonian_path(cluster_1_nodes)
    r2_base_path = solve_hamiltonian_path(cluster_2_nodes)
    
    return G, r1_base_path, r2_base_path, nodes_data, coordinates, labels, centroids

def plot_standalone_kmeans(coordinates, labels, centroids, nodes_data):
    """
    Plots a pure, dedicated 2D machine learning scatter plot of the K-Means clustering output,
    complete with spatial decision regions and calculated cluster centroids.
    """
    plt.figure(figsize=(10, 8))
    
    # Generate background color mesh grids to show the clear classification partition
    x_min, x_max = 0, 100
    y_min, y_max = 0, 100
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.5), np.arange(y_min, y_max, 0.5))
    
    # Temporary classifier initialization to paint the background decision boundaries
    temp_km = KMeans(n_clusters=2, random_state=42, n_init=10).fit(coordinates)
    Z = temp_km.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Display the separate shaded classification territories
    plt.imshow(Z, interpolation='nearest', extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Pastel2, aspect='auto', origin='lower')

    # Scatter plot the equipment node points based on their assigned clusters
    color_map = np.array(['#22c55e', '#ea580c']) # Green and Orange cluster tokens
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=color_map[labels], s=300, 
                edgecolors='#0f172a', linewidths=2.0, zorder=3)

    # Plot the calculated K-Means cluster centroids as distinct stars
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=400, c='black', 
                edgecolors='white', linewidths=1.5, zorder=4, label='Cluster Centroids')

    # Add Equipment Name labels next to each data point coordinate
    for nid, data in nodes_data.items():
        plt.text(data["pos"][0] + 1.5, data["pos"][1] + 1.5, f"N{nid}: {data['name']}", 
                 fontsize=9, fontweight='bold', zorder=5)

    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(True, linestyle=':', color='#94a3b8', alpha=0.6)
    plt.title("STANDALONE K-MEANS SPATIAL SEGREGATION DIALECT", fontsize=12, fontweight='bold', pad=15)
    plt.xlabel("Plant X-Coordinate Feature Space (Meters)", fontweight='bold')
    plt.ylabel("Plant Y-Coordinate Feature Space (Meters)", fontweight='bold')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

def visualize_central_assignments(G, path_r1, path_r2):
    """
    Renders the sequential network graph tracks after assignments.
    """
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.set_facecolor('#f8fafc')
    pos = nx.get_node_attributes(G, 'pos')
    
    nx.draw_networkx_edges(G, pos, edge_color='#e2e8f0', width=1.5, arrows=False, ax=ax)
    
    node_colors = ['#a7f3d0' if node in path_r1 else '#ffedd5' for node in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=850, edgecolors='#1e293b', linewidths=2.0, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    
    edges_r1 = [(path_r1[i], path_r1[i+1]) for i in range(len(path_r1)-1)]
    edges_r2 = [(path_r2[i], path_r2[i+1]) for i in range(len(path_r2)-1)]
    
    for u, v in edges_r1:
        ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="#1d4ed8", lw=3.0, mutation_scale=20))
    for u, v in edges_r2:
        ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="#ea580c", lw=3.0, mutation_scale=20))

    ax.plot([], [], color="#1d4ed8", lw=3.0, label="Robot 1 Baseline Path")
    ax.plot([], [], color="#ea580c", lw=3.0, label="Robot 2 Baseline Path")
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle=':', color='#cbd5e1')
    ax.set_title("PHASE 1: TOPOLOGICAL DUAL-HAMILTONIAN PATH ROUTING NETWORK", fontsize=11, fontweight='bold', pad=15)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    graph, path_r1, path_r2, raw_nodes, coords, clusters, centers = generate_centralized_baseline_map()
    print("--- HAMP-IN OBJECTIVE INITIALIZED ---")
    print(f"Robot 1 Pre-Planned Sequence: {path_r1}")
    print(f"Robot 2 Pre-Planned Sequence: {path_r2}")
    
    # 1. Trigger isolated mathematical clustering plot
    plot_standalone_kmeans(coords, clusters, centers, raw_nodes)
    
    # 2. Trigger the NetworkX structure map window
    visualize_central_assignments(graph, path_r1, path_r2)