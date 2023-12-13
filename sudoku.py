import random, copy


def initialize_population(size, input_matrix):
    population = []
    for _ in range(size):
        chromosome = [row[:] for row in input_matrix]  # Copy the input matrix
        for i in range(9):
            for j in range(9):
                if chromosome[i][j] == 0:
                    chromosome[i][j] = random.randint(1, 9)
                    zero_values.append([i, j])

        population.append(chromosome)
    return copy.deepcopy(population)


def evaluate_fitness(chromosome):
    set_col = set()
    set_block = set()
    set_row = set()
    conflicts = 0
    for i in range(9):
        for j in range(9):
            set_row.add(chromosome[i][j])
        conflicts += 9 - len(set_row)
        set_row.clear()
    for j in range(9):
        for i in range(9):
            set_col.add(chromosome[i][j])
        conflicts += 9 - len(set_col)
        set_col.clear()
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            for x in range(i, i + 3):
                for y in range(j, j + 3):
                    set_block.add(chromosome[x][y])
            conflicts += 9 - len(set_block)
            set_block.clear()
    return conflicts


def crossover(parent1, parent2):
    crossover_point = random.randint(1, 8)
    child1 = [row[:crossover_point] + parent2[row_i][crossover_point:] for row_i, row in enumerate(parent1)]
    child2 = [row[:crossover_point] + parent1[row_i][crossover_point:] for row_i, row in enumerate(parent2)]
    # child1 = parent1[:crossover_point] + parent2[crossover_point:]
    # child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return copy.deepcopy(child1), copy.deepcopy(child2)


def mutate(chromosome):
    item = random.choice(zero_values)
    chromosome[item[0]][item[1]] = random.randint(1, 9)
    return copy.deepcopy(chromosome)


def genetic_algorithm(input_matrix, population_size, generations, mutation_rate):
    population = initialize_population(population_size, input_matrix)
    for generation in range(generations):
        old = evaluate_fitness(population[0])
        population = sorted(population, key=evaluate_fitness)
        new = evaluate_fitness(population[0])
        if new != old:
            print("fitness function: ", new)
        if evaluate_fitness(population[0]) == 0:
            print("Solution found in generation", generation)
            return population[0]
        new_population = copy.deepcopy(population[:2])
        for _ in range(population_size // 2 - 1):
            parent1, parent2 = random.choices(population[:15], k=2)
            child1, child2 = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child1 = mutate(child1)
                child2 = mutate(child2)

            new_population.extend([child1, child2])
        population = copy.deepcopy(new_population)
    print("Solution not found")
    return population[0]


# Example usage
initial_hard = [
    [0, 0, 3, 0, 5, 0, 0, 2, 0],
    [0, 0, 7, 0, 0, 0, 0, 8, 0],
    [0, 0, 9, 3, 7, 0, 0, 0, 4],
    [0, 0, 5, 0, 6, 0, 9, 0, 0],
    [2, 0, 0, 0, 3, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 7, 0, 0, 0],
    [5, 0, 0, 0, 0, 6, 0, 0, 8],
    [1, 0, 0, 0, 4, 0, 0, 6, 0]
]
initial_medium = [
    [0, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 8, 1, 3, 2, 4, 7],
    [0, 8, 3, 0, 0, 0, 0, 1, 0],
    [8, 0, 0, 3, 5, 0, 4, 9, 0],
    [0, 0, 1, 7, 0, 4, 0, 0, 3],
    [3, 0, 0, 0, 0, 6, 0, 0, 0],
    [9, 0, 7, 0, 4, 2, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 9, 0, 1],
    [0, 0, 0, 6, 0, 9, 0, 2, 4]
]
initial_easy = [
    [5, 0, 3, 2, 0, 0, 1, 0, 0],
    [0, 0, 6, 0, 0, 7, 8, 0, 2],
    [1, 0, 0, 3, 0, 0, 7, 0, 5],
    [3, 5, 1, 0, 0, 2, 0, 8, 4],
    [0, 0, 7, 0, 4, 0, 6, 1, 0],
    [4, 6, 0, 8, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 5, 6, 1],
    [0, 0, 2, 4, 1, 5, 0, 7, 0],
    [8, 0, 5, 0, 6, 0, 0, 0, 0]
]

zero_values = []
solution = genetic_algorithm(initial_hard, population_size=50, generations=1000, mutation_rate=0.3)
print("Sudoku Solution:")
for row in solution:
    print(row)
