import matplotlib.pyplot as plt
import networkx as nx

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_facecolor('#f0f7fc')

nodes_data = {
    1:  {"name": "Intake",       "pos": (15, 75), "risk": 0.10, "type": "Raw Material Input"},
    2:  {"name": "Storage",      "pos": (35, 75), "risk": 0.15, "type": "Storage Racks"},
    3:  {"name": "Compressor_1", "pos": (15, 45), "risk": 0.45, "type": "Air Compressors A"},
    4:  {"name": "Boiler",       "pos": (50, 75), "risk": 0.60, "type": "Industrial Boiler"},
    5:  {"name": "Compressor_2", "pos": (15, 15), "risk": 0.45, "type": "Air Compressors B"},
    6:  {"name": "Assembly",     "pos": (35, 15), "risk": 0.20, "type": "Main Assembly Line"},
    7:  {"name": "Pressing",     "pos": (60, 45), "risk": 0.35, "type": "Pressing Station"},
    8:  {"name": "Paint_Shop",   "pos": (70, 75), "risk": 0.90, "type": "Chemical Paint Shop"},
    9:  {"name": "Oven_1",       "pos": (50, 45), "risk": 0.85, "type": "Main Kiln Oven"},
    10: {"name": "Oven_2",       "pos": (60, 15), "risk": 0.70, "type": "Heat Treatment Oven"},
    11: {"name": "Quality",      "pos": (85, 45), "risk": 0.10, "type": "Quality Check Line"},
    12: {"name": "Output",       "pos": (90, 75), "risk": 0.05, "type": "Finished Goods Hub"}
}

G = nx.DiGraph()
for node, data in nodes_data.items():
    G.add_node(node, pos=data["pos"])

edges_with_weights = [
    (1, 2, 0.015), (2, 4, 0.020), (4, 8, 0.025), (8, 12, 0.025),
    (1, 3, 0.015), (3, 5, 0.015), (5, 6, 0.015), (6, 10, 0.025),
    (10, 11, 0.025), (12, 11, 0.015), (1, 9, 0.025), (9, 4, 0.020),
    (4, 9, 0.015), (9, 7, 0.015), (7, 8, 0.025), (8, 11, 0.015),
    (3, 9, 0.015), (9, 10, 0.029), (7, 10, 0.009)
]

for u, v, w in edges_with_weights:
    G.add_edge(u, v, weight=w)

pos = nx.get_node_attributes(G, 'pos')

nx.draw_networkx_edges(
    G, pos, 
    arrowstyle='->', 
    arrowsize=18, 
    edge_color='#1a1a1a', 
    width=2.0, 
    ax=ax
)

nx.draw_networkx_nodes(
    G, pos, 
    node_color='#ffffff', 
    node_size=900, 
    edgecolors='#000000', 
    linewidths=2.0, 
    ax=ax
)

nx.draw_networkx_labels(
    G, pos, 
    font_size=11, 
    font_weight='bold', 
    font_color='#000000', 
    ax=ax
)

edge_labels = {(u, v): f"{d['weight']:.3f} kms" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(
    G, pos, 
    edge_labels=edge_labels, 
    font_size=8, 
    font_color='#2b2b2b', 
    label_pos=0.5,
    rotate=True,
    bbox=dict(facecolor='#ffffff', edgecolor='none', alpha=0.8, pad=1.0),
    ax=ax
)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_xticks(range(0, 101, 10))
ax.set_yticks(range(0, 101, 10))
ax.grid(True, which='both', color='#d0e2f0', linestyle='--', linewidth=0.8)

# 10. Titles and Axis Configurations
ax.set_title("INDUSTRIAL FACILITY NODE-EDGE TOPOLOGY MAP", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("X-Coordinate (Meters Scale)", fontsize=10, fontweight='bold')
ax.set_ylabel("Y-Coordinate (Meters Scale)", fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()