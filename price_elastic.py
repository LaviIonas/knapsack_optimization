import random

# helper
def sort_key(candidate):
    string, weight, value, under_limit = candidate
    if under_limit:
        return(0, -value)
    else:
        return(1, weight)
    
def single_point_crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        # Choose a random crossover point
        crossover_point = random.randint(1, len(parent1) - 1)
        
        # Create offspring by swapping segments
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        child1, child2 = parent1, parent2

    # mutate children
    child1 = mutate(child1, mutation_rate)
    child2 = mutate(child2, mutation_rate)
    
    return child1, child2

def mutate(genome, mutation_rate):
    mutated = ""
    for bit in genome:
        if random.random() < mutation_rate:
            # Flip the bit
            mutated += "1" if bit == "0" else "0"
        else:
            mutated += bit
    return mutated

def adjust_value(items, popularity):
    for n, i in enumerate(items):
        i['value'] = i['value'] + (i['elasticity'] * (popularity[n]/population_num))

    return items

items = [
    {"weight": 2, "value": 10, "elasticity": -1.0},  # value = 10 - 1.0 * popularity
    {"weight": 3, "value": 8,  "elasticity": -0.8},
    {"weight": 4, "value": 15, "elasticity": -2.0},
    {"weight": 5, "value": 4,  "elasticity": 0.5},  # value rises with use (network effect)
    {"weight": 1, "value": 2,  "elasticity": 0.0},   # fixed value
]
capacity = 10

# EC params
gen=10
mutation_rate = 0.01
crossover_rate = 0.8

# Create starting population
'''
genome representation: '010101' of length N where N is number of items
'''

population_num = 100
population = []

'''
create a completely random set
'''
for _ in range(population_num):
    string = ''
    for item in items:
        string += random.choice(["0","1"])
    population.append(string)

# Generational Logic
def evolutionary_step(population, items):
    random.shuffle(population)

    popularity = [0,0,0,0,0]

    # Fitness Function
    fitness_score = []
    for p in population:
        value = 0
        weight = 0
        for j, choice in enumerate(p):
            if choice == "1":
                popularity[j] += 1
                value += items[j]['value']
                weight += items[j]['weight']
        fitness_score.append((weight, value))

    # Selection 
    # 4 parent tournament
    parents = []
    for j in range(0, len(population), 4):
        tournament = population[j:j+4]
        scores = fitness_score[j:j+4]


        candidates = []
        for j, (string, (weight, value)) in enumerate(zip(tournament, scores)):
            under_limit = weight <= capacity
            candidates.append((string, weight, value, under_limit))

        top_candidates = sorted(candidates,key=sort_key)[:2]
        for string, weight, value, under_limit in top_candidates:
            parents.append(string)

    # present generation best mf
    highest_scoring = sorted(candidates,key=sort_key)[:5]

    # Crossover
    # randomize parents
    random.shuffle(parents)
    survivors = []
    for j in range(0, len(parents), 2):
        parent1 = parents[j]
        parent2 = parents[j+1]

        child1, child2 = single_point_crossover(parent1, parent2, crossover_rate)

        survivors.append(parent1)
        survivors.append(parent2)
        survivors.append(child1)
        survivors.append(child2)


    return survivors, highest_scoring, popularity

surviors, highest_score, popularity = evolutionary_step(population, items)
print("GENERATION 0")
for string, weight, value, under_limit in highest_score:
    print(string + " value: " + str(value) + " weight: " + str(weight))

print(popularity)
items = adjust_value(items, popularity)
print(items)

# generational loop
for i in range(gen):
    surviors, highest_score, popularity = evolutionary_step(surviors, items)
    items = adjust_value(items, popularity)
    print(items)
    print("GENERATION ", i)
    for string, weight, value, under_limit in highest_score:
        print(string + " value: " + str(value) + " weight: " + str(weight))


