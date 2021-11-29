import copy
import random

import matplotlib
import matplotlib.pyplot
import numpy

import src.dimensions as D


# Genetic Algorithm methods

def local_fitness(field, x, y, plants_case):
    soil_value = 0
    if field[x][y].field_type == "soil":
        soil_value = 1
    else:
        soil_value = 0.5

    if plants_case[x][y] == "":
        plant_value = 0
    elif plants_case[x][y] == "w":
        plant_value = 1
    elif plants_case[x][y] == "p":
        plant_value = 2
    elif plants_case[x][y] == "s":
        plant_value = 3
    else:
        plant_value = 1

    neighbour_bonus = 1

    if x - 1 >= 0:
        if plants_case[x][y] == plants_case[x - 1][y]:
            neighbour_bonus += 1
    if x + 1 < D.GSIZE:
        if plants_case[x][y] == plants_case[x + 1][y]:
            neighbour_bonus += 1
    if y - 1 >= 0:
        if plants_case[x][y] == plants_case[x][y - 1]:
            neighbour_bonus += 1
    if y + 1 < D.GSIZE:
        if plants_case[x][y] == plants_case[x][y + 1]:
            neighbour_bonus += 1

    local_fitness_value = (soil_value + plant_value) * (0.5 * neighbour_bonus + 1)
    return local_fitness_value


def population_fitness(population_text_local, field, population_size):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    fitness = []

    for k in range(population_size):
        population_values_single = []
        population_values_single_row = []
        fitness_row = []

        for i in range(0, D.GSIZE):
            for j in range(0, D.GSIZE):
                population_values_single_row.append(local_fitness(field, i, j, population_text_local))
            population_values_single.append(population_values_single_row)

        for i in range(D.GSIZE):
            fitness_row.append(sum(population_values_single[i]))
        fitness = sum(fitness_row)
    return fitness


def crossover(local_parents):
    ret = []
    for i in range(0, len(local_parents)):
        child = copy.deepcopy(local_parents[i])
        # Vertical randomization
        width = random.randint(1, D.GSIZE // len(local_parents))  # width of stripes
        indexes_parents = numpy.random.permutation(range(0, len(local_parents)))  # sorting of stripes
        beginning = random.randint(0, len(local_parents[0]) - width * len(
            local_parents))  # point we start putting the stripes from
        for x in indexes_parents:
            child[beginning:beginning + width] = local_parents[x][beginning:beginning + width]
            beginning += width
        ret.append(child)
    return ret


def mutation(population_units, offspring_crossover, num_mutants, num_mutations=10):
    for case in range(0, len(offspring_crossover)):
        for mutation in range(0, num_mutations):
            mutation_x = random.randint(0, D.GSIZE - 1)
            mutation_y = random.randint(0, D.GSIZE - 1)
            mutation_value = random.choice(population_units)
            offspring_crossover[case][mutation_x][mutation_y] = mutation_value
            num_mutants -= 1

    return offspring_crossover


def pretty_printer(best_outputs):
    matplotlib.pyplot.plot(best_outputs)
    matplotlib.pyplot.xlabel("Iteration")
    matplotlib.pyplot.ylabel("Fitness")
    matplotlib.pyplot.show()
