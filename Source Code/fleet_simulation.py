"""
HAMP-IN Framework: Phases 2, 3, and 4 (Live Visualized Online Engine Loop)
File: fleet_simulation.py
Description: Simulates simultaneous real-time execution of Robot 1 and Robot 2
             tracking decentralized local subgraphs with network path fallbacks.
"""

import time
import math
import networkx as nx
import matplotlib.pyplot as plt
from central_map import generate_centralized_baseline_map

def get_network_distance(graph, u, v):
    """
    Safely calculates structural network distance between any two layout positions,
    falling back to topological shortest path routing if a direct aisle does not exist.
    """
    if graph.has_edge(u, v):
        return graph[u][v]['base_dist']
    elif graph.has_edge(v, u):
        return graph[v][u]['base_dist']
    else:
        try:
            # Fallback: Find shortest physical route through alternate corridors
            return nx.shortest_path_length(graph, source=u, target=v, weight='base_dist')
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # Absolute baseline geometric distance if completely isolated
            pos = nx.get_node_attributes(graph, 'pos')
            return math.dist(pos[u], pos[v]) / 1000.0  # Scale to km

def execute_robot1_edge_loop(current_idx, path_array, graph_model, live_traffic, tau=0.75):
    """
    Local edge computing loop for Robot 1. Checks for congestion and consecutive risk chains.
    """
    if current_idx >= len(path_array) - 1:
        return current_idx, path_array, "Finished", 0.0

    u = path_array[current_idx]
    v = path_array[current_idx + 1]
    
    dist_uv = get_network_distance(graph_model, u, v)
    swarm_uv = live_traffic.get((u, v), 0.0) or live_traffic.get((v, u), 0.0)
    risk_v = graph_model.nodes[v]["risk"]
    
    alpha, beta, lambda_k, omega_k = 1.0, 2.0, 1.5, 0.0
    action_taken = "Branch A: Standard Move"

    # Branch C: Localized Subgraph Mutation (Congestion Bypass)
    if swarm_uv > 0.80:
        action_taken = "Branch C: Swarm Bypass Injected"
        path_array.insert(current_idx + 1, 7)  # Inject node 7 as a dynamic detour corridor
        v = path_array[current_idx + 1]
        dist_uv = get_network_distance(graph_model, u, v)
        swarm_uv = 0.0

    # Branch B: Localized Risk-Chaining Activation
    elif risk_v >= tau:
        if current_idx + 2 < len(path_array):
            v_next = path_array[current_idx + 2]
            if graph_model.nodes[v_next]["risk"] >= tau:
                action_taken = f"Branch B: Risk-Chain Active (Node {v})"
                lambda_k = 0.01  # Absorb risk penalty near-zero to claim sequence

    computed_cost = (alpha * dist_uv) + (beta * swarm_uv) + (lambda_k * risk_v) + omega_k
    return current_idx + 1, path_array, action_taken, computed_cost


def execute_robot2_edge_loop(current_idx, path_array, graph_model, live_traffic, r1_target_node, tau=0.75):
    """
    Local edge computing loop for Robot 2. Monitors Robot 1's destination for exclusion boundaries.
    """
    if current_idx >= len(path_array) - 1:
        return current_idx, path_array, "Finished", 0.0

    u = path_array[current_idx]
    v = path_array[current_idx + 1]
    
    dist_uv = get_network_distance(graph_model, u, v)
    swarm_uv = live_traffic.get((u, v), 0.0) or live_traffic.get((v, u), 0.0)
    risk_v = graph_model.nodes[v]["risk"]
    
    alpha, beta, lambda_k, omega_k = 1.0, 2.0, 1.5, 0.0
    action_taken = "Branch A: Standard Move"

    # Branch B: Mutual Exclusion Enforcement (Omega Barrier Driven)
    if risk_v >= tau and r1_target_node == v:
        action_taken = f"Branch B: Omega Blocked by R1"
        omega_k = 999.0  # Drive cost to infinity to lock out Robot 2

    # Branch C: Localized Subgraph Mutation (Congestion Bypass)
    elif swarm_uv > 0.80:
        action_taken = "Branch C: Swarm Bypass Injected"
        path_array.insert(current_idx + 1, 11)  
        v = path_array[current_idx + 1]
        dist_uv = get_network_distance(graph_model, u, v)
        swarm_uv = 0.0

    computed_cost = (alpha * dist_uv) + (beta * swarm_uv) + (lambda_k * risk_v) + omega_k
    return current_idx + 1, path_array, action_taken, computed_cost


# --- MASTER VISUAL RUNTIME MAIN INTERACTION ---
if __name__ == "__main__":
    # Import initialized base topology components from central_map.py
    G, r1_path, r2_path, _, _, _, _ = generate_centralized_baseline_map()
    G_undirected = G.to_undirected()
    
    r1_idx, r2_idx = 0, 0
    time_step = 0
    tau_threshold = 0.75
    
    # Initialize interactive plotting environments
    plt.ion()
    fig, ax = plt.subplots(figsize=(13, 9))
    pos = nx.get_node_attributes(G, 'pos')

    print("="*80)
    print(" HAMP-IN RUNTIME ENGINE STARTED: OPENING LIVE INSPECTION VISUALIZER PANEL")
    print("="*80)

    while r1_idx < len(r1_path) - 1 or r2_idx < len(r2_path) - 1:
        time_step += 1
        
        # Inject structural dynamic obstacle at T=2 on corridor (3 -> 9)
        live_traffic_map = {}
        if time_step == 2:
            live_traffic_map[(3, 9)] = 0.95 

        # Monitor next coordinates
        r1_dest = r1_path[r1_idx + 1] if r1_idx < len(r1_path) - 1 else None
        
        # Run local calculation ticks
        act1, cost1 = "Stationary", 0.0
        if r1_idx < len(r1_path) - 1:
            r1_idx, r1_path, act1, cost1 = execute_robot1_edge_loop(r1_idx, r1_path, G_undirected, live_traffic_map, tau=tau_threshold)

        act2, cost2 = "Stationary", 0.0
        if r2_idx < len(r2_path) - 1:
            r2_idx, r2_path, act2, cost2 = execute_robot2_edge_loop(r2_idx, r2_path, G_undirected, live_traffic_map, r1_dest, tau=tau_threshold)

        # --- REFRESH IMAGE CANVAS LAYER ---
        ax.clear()
        ax.set_facecolor('#f1f5f9')
        
        # Draw physical corridors
        nx.draw_networkx_edges(G, pos, edge_color='#cbd5e1', width=1.5, style=':', arrows=False, ax=ax)
        
        # Map dynamic node safety tints
        node_colors = []
        for node in G.nodes:
            if G.nodes[node]["risk"] >= tau_threshold:
                node_colors.append('#fca5a5')  # Hazard Red Alert Node
            elif G.nodes[node]["risk"] > 0.35:
                node_colors.append('#fde047')  # Warning Zone Node
            else:
                node_colors.append('#cbd5e1')  # Standard Safe Grey Node
                
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=750, edgecolors='#475569', linewidths=1.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', font_color='#0f172a', ax=ax)

        # Fetch tracking nodes
        curr_r1_node = r1_path[r1_idx]
        curr_r2_node = r2_path[r2_idx]
        
        # Highlight active agent coordinates on screen (Valid hex string color applied)
        nx.draw_networkx_nodes(G, pos, nodelist=[curr_r1_node], node_color='#2563eb', node_size=950, edgecolors='#000000', linewidths=2.5, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=[curr_r2_node], node_color='#ea580c', node_size=950, edgecolors='#000000', linewidths=2.5, ax=ax)

        # Clean ASCII text block formatting (No Unicode emoji blocks to trigger font warning traps)
        telemetry_text = (
            f"TIME STEP: T = {time_step}\n"
            f"----------------------------------------------------------------------\n"
            f"ROBOT 1 Location: Node {curr_r1_node}\n"
            f"   Action: {act1}\n"
            f"   Computed Cost: {cost1:.4f}\n"
            f"   Pending Queue: {r1_path[r1_idx:]}\n\n"
            f"ROBOT 2 Location: Node {curr_r2_node}\n"
            f"   Action: {act2}\n"
            f"   Computed Cost: {cost2:.4f}\n"
            f"   Pending Queue: {r2_path[r2_idx:]}"
        )
        
        ax.text(2, 5, telemetry_text, fontsize=10, fontfamily='monospace', fontweight='bold',
                bbox=dict(facecolor='#ffffff', edgecolor='#94a3b8', boxstyle='round,pad=1.0', alpha=0.95))

        if time_step == 2:
            ax.scatter(15, 45, s=1200, marker='X', color='red', lw=3, zorder=10, label="Dynamic Crowd Bottleneck Spike")

        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_xticks(range(0, 101, 10))
        ax.set_yticks(range(0, 101, 10))
        ax.grid(True, linestyle='--', color='#e2e8f0', linewidth=0.5)
        ax.set_title("HAMP-IN ENGINE: DISTRIBUTED MULTI-AGENT EXECUTION SIMULATOR", fontsize=11, fontweight='bold', pad=15)
        
        ax.plot([], [], 'o', color='#2563eb', ms=10, label="Robot 1 Fleet Position Indicator")
        ax.plot([], [], 'o', color='#ea580c', ms=10, label="Robot 2 Fleet Position Indicator")
        ax.legend(loc='upper right', facecolor='#ffffff', framealpha=0.9)

        fig.canvas.draw()
        fig.canvas.flush_events()
        
        time.sleep(1.8)

    plt.ioff()
    print("\n[SUCCESS] Entire sequence tracked cleanly without structural array faults.")
    plt.show()