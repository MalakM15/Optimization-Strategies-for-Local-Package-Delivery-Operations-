# Local Package Delivery Optimization
This project implements two optimization algorithms ( Genetic Algorithm (GA) and Simulated Annealing (SA))to solve a constrained Vehicle Routing Problem (VRP). The goal is to optimize local package delivery by minimizing travel distance while adhering to vehicle capacities and delivery priorities.
---
## 🚀 Problem Statement
The objective is to assign a set of packages to a set of vehicles such that:
* **Total Distance** traveled is minimized.
* **Vehicle Capacity** is never exceeded (**Hard Constraint**).
* **High-Priority Packages** are delivered first whenever possible (**Soft Constraint** via penalty-based evaluation).

---
## 🧠 Algorithms Implemented

### 1️⃣ Genetic Algorithm (GA)
The GA evolves a population of solutions over generations using operators inspired by evolutionary biology:

* **Individual Representation:** A dictionary mapping **Vehicle IDs** to a list of assigned packages.
* **Selection:** **Tournament Selection** where a subset is randomly chosen, and the fittest individual (lowest cost) moves to the next generation.
* **Crossover:** Routes from two parents are merged, ensuring **all packages are assigned exactly once** with no duplicates.
* **Mutation:** Randomly **reorders packages** within a vehicle to explore non-priority-ordered sequences that might yield shorter paths.

### 2️⃣ Simulated Annealing (SA)
SA explores the solution space by mimicking the thermodynamic cooling process of metals:

* **Neighbor Generation:** Small stochastic changes, such as **swapping packages** between vehicles or moving a package to a different route.
* **Acceptance Criteria:** Always accepts better solutions; accepts worse solutions based on the **Boltzmann probability** ($e^{-\Delta E / T}$) to avoid local optima.
* **Cooling Schedule:** An **exponential decay** model that reduces the system "temperature" over time to stabilize the solution.

---

## 📊 Parameters & Configuration

| Parameter | Value |
| :--- | :--- |
| **Initial Temperature** | `1000` |
| **Cooling Rate** | `0.95` |
| **Max Iterations (SA)** | `100` |
| **Population Size** | `75` |
| **Generations** | `500` |
| **Mutation Rate** | `0.75` |
| **Tournament Ratio** | `0.2` |

---

## 📈 Results & Conclusions
The project findings demonstrate distinct strengths for each approach:

* **GA Efficiency:** Highly effective at finding **global optima** by maintaining a diverse population, though it requires more computational time.
* **SA Speed:** Significantly **faster** and excellent at escaping local optima through its probabilistic acceptance of worse moves at high temperatures.
* **Constraint Handling:** **Penalty Functions** successfully guided both algorithms to respect package priorities without making the search space too rigid for optimization.

---

## 👥 Team Members
* **Malak Milhem** &  **Maysam Habbash** 
