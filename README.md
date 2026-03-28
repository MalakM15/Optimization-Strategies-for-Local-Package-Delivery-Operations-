Local Package Delivery Optimization
This project implements two optimization algorithms ( Genetic Algorithm (GA) and Simulated Annealing (SA))to solve a constrained Vehicle Routing Problem (VRP). The goal is to optimize local package delivery by minimizing travel distance while adhering to vehicle capacities and delivery priorities.

🚀 Problem Statement
The objective is to assign a set of packages to a set of vehicles such that:

Total Distance traveled is minimized.

Vehicle Capacity is never exceeded (hard constraint).

High-priority packages are delivered first whenever possible (soft constraint/penalty-based).

🧠 Algorithms Implemented
1. Genetic Algorithm (GA)
The GA evolves a population of solutions over generations using biological operators:

Individual Representation: A dictionary mapping vehicle IDs to a list of assigned packages.

Selection: Tournament Selection where a subset is randomly chosen, and the fittest individual (lowest cost) moves to the next generation.

Crossover: Routes from two parents are merged, ensuring all packages are assigned exactly once.

Mutation: Randomly reorders packages within a vehicle to explore non-priority-ordered sequences that might yield shorter paths.

2. Simulated Annealing (SA)
SA explores the solution space by mimicking the cooling process of metals:

Neighbor Generation: Small stochastic changes (swapping packages or moving a package between vehicles).

Acceptance Criteria: Always accepts better solutions; accepts worse solutions based on the Boltzmann probability.
 
Cooling Schedule

📊 Parameters & Configuration
Parameter	Value
Initial Temperature	1000
Cooling Rate	0.95
Max Iterations (SA)	100
Population Size	75
Generations	500
Mutation Rate	0.75
Tournament Ratio	0.2

📈 Results
The project demonstrates that:

GA is highly effective at finding global optima by maintaining a diverse population but requires more computational time.

SA is faster and excellent at escaping local optima through its probabilistic acceptance of worse moves at high temperatures.

Penalty Functions successfully guided both algorithms to respect package priorities without making the search space too rigid.

Team Members: Malak Milhem & Maysam Habbash
