<img width="4605" height="105" alt="image" src="https://github.com/user-attachments/assets/ab538bff-40e9-4c55-8585-d97f136d3396" /># HAMP-IN-
HAMILTONIAN PATH-BASED MULTI-ROBOT INSPECTION FRAMEWORK WITH SWARM-OCCUPANCY TRACKING AND RISK MITIGATION

Risk-Aware Multi-Agent Hamiltonian Path Planning with Swarm-Occupancy Cost Modulation for Industrial Facility Inspection

Main Idea of this Research :
 # ALGORITHMIC RISK-CHAINING - If node u was already classified as a high-risk zone and its adjacent neighbor 𝑣 is also flagged as a high-risk zone (𝑅(𝑣)>𝜏),the algorithm activates Risk-Chaining. 
 <img width="1511" height="257" alt="image" src="https://github.com/user-attachments/assets/6f08ab91-c51c-42da-91ce-77fca5a9c597" />

 # Algorithmic Lookahead Module -The Lookahead Protocol
Node Arrival: When agent 𝑅_1successfully arrives at and completes the inspection of node 𝑢, it queries the local environmental risk values 𝑅(𝑣_𝑖 )for all immediately adjacent unvisited neighbors 𝑣_𝑖∈"Adj" (𝑢).

Hazard Threshold Evaluation: The agent checks these values against a predefined safety threshold 𝜏 .If an adjacent node 𝑣 exhibits a sudden hazard spike such that 𝑅(𝑣)>𝜏, the reactive routine is triggered.

# Dynamic Mutual Exclusion Penalty (Ω→∞) - HAMP-IN relies on a Dynamic Mutual Exclusion Penalty (Ω→∞). The two robots naturally carve out their own optimal tracks in real-time on a single directed graph, removing the single point of failure of a central master clock




