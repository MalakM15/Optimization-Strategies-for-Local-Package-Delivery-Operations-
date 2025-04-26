# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#Maysam Habbash 122007
#Malak Milhem 1220031

import re
import random
import math
import copy
from pprint import pprint
class Package:
    def __init__(self, id, x, y, weight, priority):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority

class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = []

## Global Declarations
 # lists
packages =[]
vehicles =[]
 # file names
packages_file = "C:\\Users\\HP\\Documents\\GitHub\\Artificial_Intelligence\\packages.txt"
vehicles_file = "C:\\Users\\HP\\Documents\\GitHub\\Artificial_Intelligence\\vehicles.txt"
 # genetic algorithm parameters
POPULATION_SIZE = 75
MUTATION_RATE = 0.05
GENERATIONS_COUNT = 500
TOURNAMENT_RATIO = 0.15

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def take_package_data():
    num_packages=int (input("Enter the number of packages:"))
    print("Enter the following data for all packages: -priority  -weight  -destination(x,y):")
    package_id=1
    while (num_packages > 0):
        package_priority = int(input(f" package {package_id} priority:"))
        package_weight = float(input(f" package {package_id} weight:"))
        package_destination_x = int(input(f" package {package_id} destination (x):"))
        package_destination_y = int(input(f" package {package_id} destination (y):"))
        obj_package = Package(package_id,package_destination_x,package_destination_y,package_weight,package_priority)
        packages.append(obj_package)
        num_packages=num_packages-1
        package_id=package_id+1

    for pack in packages:
        print(f"id: {pack.id}, weight: {pack.weight} ,priority:{pack.priority}")

def take_vehicle_data():
    num_vehicles = int (input("Enter the number of vehicles:"))
    vehicle_id = 1
    while (num_vehicles > 0):

        vehicle_capacity = float(input(f"Enter vehicle {vehicle_id} capacity:"))
        obj_vehicle=Vehicle(vehicle_id, vehicle_capacity)
        vehicles.append(obj_vehicle)
        num_vehicles = num_vehicles - 1
        vehicle_id = vehicle_id + 1
    for v in vehicles:
        print(f"id: {v.id}, capacity: {v.capacity}")


def generate_random_initial_state(packages, vehicles):
        while True:
            solution = {v.id: [] for v in vehicles}
            vehicle_capacities = {v.id: float(v.capacity) for v in vehicles}

            unassigned = packages.copy()
            random.shuffle(unassigned)

            all_assigned = True

            for package in unassigned:
                assigned = False
                random.shuffle(vehicles)
                for v in vehicles:
                    if float(package.weight) <= vehicle_capacities[v.id]:
                        solution[v.id].append(package)
                        vehicle_capacities[v.id] -= float(package.weight)
                        assigned = True
                        break
                if not assigned:
                    all_assigned = False
                    break

            if all_assigned:
                return solution
def total_distance(solution):
        total_distance = 0.0

        for vehicle_id, packages in solution.items():
            if not packages:
                continue

            x_prev, y_prev = 0, 0  # Start from the shop

            for package in packages:
                x_curr, y_curr = float(package.x), float(package.y)
                dist = calculate_distance(x_prev, y_prev, x_curr, y_curr)
                total_distance += dist
                x_prev, y_prev = x_curr, y_curr
            # return to shop
            total_distance += calculate_distance(x_prev, y_prev, 0, 0)

        return total_distance



def generate_newsolution(solution, vehicles):
    new_solution = copy.deepcopy(solution)

    # 0 = swap between vehicles, 1 = reorder one vehicle
    move_type = random.choice([0, 1])

    if move_type == 0:
        # Swap two packages between two different vehicles
        vehicle_ids = list(new_solution.keys())
        if len(vehicle_ids) < 2:
            return new_solution  # not enough vehicles to swap

        v1, v2 = random.sample(vehicle_ids, 2)
        if not new_solution[v1] or not new_solution[v2]:
            return new_solution  # skip if any vehicle has no packages

        p1 = random.choice(new_solution[v1])
        p2 = random.choice(new_solution[v2])

        # Check weight constraint before swapping
        v1_capacity = sum(float(p.weight) for p in new_solution[v1]) - float(p1.weight) + float(p2.weight)
        v2_capacity = sum(float(p.weight) for p in new_solution[v2]) - float(p2.weight) + float(p1.weight)

        v1_full_capacity = next(v.capacity for v in vehicles if v.id == v1)
        v2_full_capacity = next(v.capacity for v in vehicles if v.id == v2)

        if v1_capacity <= v1_full_capacity and v2_capacity <= v2_full_capacity:
            new_solution[v1].remove(p1)
            new_solution[v1].append(p2)
            new_solution[v2].remove(p2)
            new_solution[v2].append(p1)

    else:
        # Reorder packages of one vehicle
        vehicle_ids = list(new_solution.keys())
        v = random.choice(vehicle_ids)
        if len(new_solution[v]) >= 2:
            random.shuffle(new_solution[v])

    return new_solution
def validate_solution(solution, vehicles):
    for v in vehicles:
        vehicle_load = sum(p.weight for p in solution[v.id])
        if vehicle_load > v.capacity:
            return False

    all_packages = [p.id for packs in solution.values() for p in packs]
    if len(all_packages) != len(set(all_packages)):
        return False

    return True

def simulated_annealing(initial_solution, vehicles):
#### algorithm parameters
    initial_temp = 1000
    stopping_temp = 1
    cooling_rate = 0.95
    iterations_per_temp = 100

    current_solution = initial_solution
    current_cost = total_distance(current_solution)
    best_solution = current_solution
    best_cost = current_cost

    T = initial_temp

    while T > stopping_temp:
        for i in range(iterations_per_temp):
            newsolution = generate_newsolution(current_solution, vehicles)
            if not validate_solution(newsolution, vehicles):
                continue  # skip invalid solution
            newsolution_cost = total_distance(newsolution)

            cost_diff = newsolution_cost - current_cost

            if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / T):
                current_solution = newsolution
                current_cost = newsolution_cost

                if current_cost < best_cost:
                    best_solution = current_solution
                    best_cost = current_cost

        T *= cooling_rate  # cool down

    return best_solution, best_cost

def display_menu():
   # print("Welcome, Choose an Algorithm from the following:\n1-simulated annealing.\n2-Genetic algorithm.")
    choise= int(input( "Welcome, Choose an Algorithm from the following:\n1-simulated annealing.\n2-Genetic algorithm.\n"))

    if (choise==1):  
        take_package_data()
        take_vehicle_data()
        print("You chose Simulated Annealing.")
        initial = generate_random_initial_state(packages, vehicles)
        print("\nInitial solution:")
        for vid, packs in initial.items():
            print(f"Vehicle {vid}: {[p.id for p in packs]}")
        print(f"Initial total distance: {total_distance(initial):.2f} km")

        best_solution, best_cost = simulated_annealing(initial,vehicles)

        print("\nOptimized solution:")
        for vid, packs in best_solution.items():
            print(f"Vehicle {vid}: {[p.id for p in packs]}")
        print(f"\nOptimized total distance: {best_cost:.2f} km")

    elif(choise==2):
        genetic_algorithm()
    else:
        print("Invalid algorithm!\n")

## Function to upload data from file
def upload_data():
    index = 1
    # upload packages from file
    with open(packages_file, 'r') as file:
        for line in file:
            data = line.strip().split()
            # create object with packet data
            pkg = Package(index, int(data[2]), int(data[3]), int(data[1]), int(data[0]))
            packages.append(pkg)
            index += 1
    
    index = 1 # reset index
    # upload vehicles from file
    with open(vehicles_file, 'r') as file:
        for line in file:
            # create object with vehicle data
            vehicle_obj = Vehicle(index, int(line))
            vehicles.append(vehicle_obj) # add to list of vehicles
            index += 1

## Function to print the uploaded data
def print_data(vehicles, packages):
    print("Vehicles:\n")
    for v in vehicles:
        print(f"id: {v.id}, capacity: {v.capacity}\n")
    
    print("\nPackages:\n")
    for p in packages:
        print(f"id: {p.id}, priority: {p.priority}, weight: {p.weight}, (x,y): ({p.x},{p.y})\n") 

## Function to generate individuals of potential solutions
def generate_individual(packages, vehicels):
    # represent individual as vehicle with ordered list (priority) of packages to deliver
    print()

## Fitness Function
def evaluate_individual():
    # evaluate based on total distance travelled by all vehicles
    print()

## Function to generate population
def generate_population(packages, vehicels):
    # generate number of individuals to form the population
    return [generate_individual(packages, vehicels) for i in range(POPULATION_SIZE)]

## Function to evaluate population
def evaluate_population(population):
    evaluated_population = []
    # evaluate each individual in the population
    for individual in population:
        evaluation = evaluate_individual(individual)
        evaluated_population.append((individual, evaluation))

    return evaluated_population

## Function to instantiate a tournament among individuals in generation
def instantiate_tournament(generation):
    # take a subset from generation for tournament
    tournament_size = round(len(generation) * TOURNAMENT_RATIO)
    tournament = random.sample(generation, tournament_size)
    ############################################################# revise key for sort ##################33
    tournament.sort(key=lambda pair: pair[1])

    return tournament[0] # return winner of the tournament

## Function to select generation
def select_generation(generation):
    selected = []
    while len(selected) < len(generation):
        # append winner of the tournament to list of selected individuals in generation
        selected.append(instantiate_tournament(generation, TOURNAMENT_RATIO))

    return selected

## Function to simulate crossover operator
def crossover_generation(population):
    print()

## Function to simulate mutations
def mutate_generation(generation):
    new_generation = []

    for individual in generation:
        # all individuals have chance in mutation
        individual = mutate(individual, MUTATION_RATE)
        new_generation.append(individual)

    return new_generation

## Function to perform mutation on individual
def mutate(individual):
    # change order of packages in a vehicle

    # EXAMPLE
    # for index in range(len(individual)):
    #     if random.random() < chance:
    #         individual[index] = random.uniform(*parameter_bounds)

    return individual

## Function to report current best solution
def report(population, best_individual, generation):
    evaluation = [item[1] for item in population]
    population.sort(key=lambda pair: pair[1])
    current_best = population[0]

    if current_best[1] < best_individual[1]:
        # better total cost found
        best_individual = current_best
    
    print('[', generation, ']\t',
          sum(evaluation) / len(evaluation), 
          '\tbest:', current_best[1])

    return best_individual

## Function to run genetic algorithm
def genetic_algorithm():
    upload_data()
    print_data(vehicles, packages)

    history = [] # preserve history of best solutions
    # create initial population
    population = generate_population()
    population = evaluate_population(population)
    # initial best solution
    best_solution = report(population, (_, float('inf')), 0)
    history.append(best_solution)

    for generation in range(1, GENERATIONS_COUNT):
        # select operator
        population = select_generation(population)
        # crossover operator
        population = crossover_generation(population)
        # mutate operator
        population = mutate_generation(population)

        # reevaluate best solution
        population = evaluate_population(population)
        best_solution = report(population, best_solution, generation)
        
        history.append(best_solution)

## Main Function to run the program
def main():
    display_menu()

if __name__ == "__main__":
    main()