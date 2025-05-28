import random 

items = [
    {"item_id": "A", "a": 100, "b": 2, "p_min": 1, "p_max": 20},
    {"item_id": "B", "a": 80,  "b": 1, "p_min": 2, "p_max": 25},
    {"item_id": "C", "a": 120, "b": 3, "p_min": 1, "p_max": 15},
    {"item_id": "D", "a": 30,  "b": 5, "p_min": 5, "p_max": 30},
    {"item_id": "E", "a": 150, "b": 4, "p_min": 3, "p_max": 20},
    {"item_id": "F", "a": 90,  "b": 2, "p_min": 1, "p_max": 18},
    {"item_id": "G", "a": 70,  "b": 1.5, "p_min": 2, "p_max": 22},
    {"item_id": "H", "a": 110, "b": 2.5, "p_min": 1, "p_max": 17},
    {"item_id": "I", "a": 95,  "b": 1.8, "p_min": 1, "p_max": 19},
    {"item_id": "J", "a": 85,  "b": 1.2, "p_min": 2, "p_max": 24},
]

weight_max = 20

def calculate_weight_inverse(a, b, p):
    return a / (b * p)

def generate_individual(items):
    individual = []
    for item in items:
        x_i = random.randint(0, 1)
        p_i = random.uniform(item["p_min"], item["p_max"])
        individual.append((x_i, p_i))
    return individual

def fitness(individual, items, weight_max):
    total_weight = 0
    total_profit = 0

    for i, (x_i, p_i) in enumerate(individual):
        if x_i == 0:
            continue
        a_i = items[i]["a"]
        b_i = items[i]["b"]
        w_i = a_i / (b_i + p_i)
        # print(f"Item {items[i]['item_id']}: price={p_i:.2f}, weight={w_i:.2f}, profit={p_i * w_i:.2f}")

        total_weight += w_i
        total_profit += p_i * w_i

    is_valid = total_weight <= weight_max

    if is_valid:
        usage_ratio = total_weight / weight_max
        total_profit *= (0.9 + 0.1 * usage_ratio)  # boost profit slightly if closer to full weight

    return total_profit, total_weight, is_valid

def structured_tournament_selection(population, items, weight_max, k=4):
    assert len(population) % k == 0

    selected = []

    for i in range(0, len(population), k):
        group = population[i:i+k]
        evaluated = [(ind, *fitness(ind, items, weight_max)) for ind in group]
        evaluated.sort(key=lambda x: (not x[3], -x[1]))  # prioritize valid, then highest profit
        
        # best of group
        selected.append(evaluated[0][0])  
        selected.append(evaluated[1][0])

    return selected  # return a list of best individuals

def crossover(parent1, parent2):
    child = []
    for (x1, p1), (x2, p2) in zip(parent1, parent2):
        if random.random() < 0.5:
            child.append((x1, p1))
        else:
            child.append((x2, p2))
    return child

def mutate(individual, items, x_prob=0.05, p_prob=0.1):
    mutated = []
    for i, (x_i, p_i) in enumerate(individual):
        # Flip selection bit
        if random.random() < x_prob:
            x_i = 1 - x_i

        # Mutate price
        if random.random() < p_prob:
            p_min = items[i]["p_min"]
            p_max = items[i]["p_max"]
            p_i = random.uniform(p_min, p_max) 

        mutated.append((x_i, p_i))
    return mutated

# Generate a population of 100 individuals
population_size = 100
population = [generate_individual(items) for _ in range(population_size)]

def evolve(population, items, weight_max, gen=100):
    for gen in range(gen):
        selected = structured_tournament_selection(population, items, weight_max, k=4)
        next_gen = []

        evaluated = [(ind, *fitness(ind, items, weight_max)) for ind in population]
        valid = [x for x in evaluated if x[3]]  # x[3] is is_valid

        if valid:
            valid.sort(key=lambda x: -x[1])  # sort by profit descending
            top1, top2 = valid[0], valid[1] if len(valid) > 1 else valid[0]

            print(f"Gen {gen+1:2d} Top 1: Profit={top1[1]:.2f}, Weight={top1[2]:.2f}")
            print(f"Gen {gen+1:2d} Top 2: Profit={top2[1]:.2f}, Weight={top2[2]:.2f}")
        else:
            print(f"Gen {gen+1:2d}: No valid individuals")

        random.shuffle(selected)

        for i in range(0, len(selected), 2):
            parent1 = selected[i]
            parent2 = selected[i+1]

            child1 = mutate(crossover(parent1, parent2), items)
            child2 = mutate(crossover(parent2, parent1), items)

            next_gen.extend([child1, child2, parent1, parent2])

        population = next_gen  # replace entire population

    return population

evolve(population, items, weight_max)