import keyboard as keyboard

import field as F
from ga_methods import *
from src import mapschema as maps


# Genetic Algorithm
def genetic_algorithm_setup(field):
    population_units = ["", "w", "p", "s"]

    # TODO REPREZENTACJA OSOBNIKA - MACIERZ ROZKłADU PLONÓW
    population_text = []
    population_text_single = []

    population_size = 10

    # Populate the population_text array
    for k in range(population_size):
        population_text_single = []
        for row in range(D.GSIZE):
            population_text_single.append([])
            for column in range(D.GSIZE):
                population_text_single[row].append(random.choice(population_units))
        population_text.append(population_text_single)

    """
    Genetic algorithm parameters:
        Mating pool size
        Population size
    """

    # units per population in generation
    best_outputs = []
    num_generations = 100
    num_parents = 4

    # iterative var
    generation = 0
    stop = 0
    # TODO WARUNEK STOPU
    while generation < num_generations and stop < 3:
        if keyboard.is_pressed('space'):
            generation += 1

            print("Generation : ", generation)
            # Measuring the fitness of each chromosome in the population.

            # population Fitness
            fitness = []

            for i in range(0, population_size):
                fitness.append((i, population_fitness(population_text[i], field, population_size)))

            print("Fitness")
            print(fitness)

            best = sorted(fitness, key=lambda tup: tup[1], reverse=True)[0:num_parents]

            # Leaderboard only
            best_outputs.append(best[0][1])

            # The best result in the current iteration.
            print("Best result : ", best[0])

            # TODO METODA WYBORU OSOBNIKA - RANKING
            # Selecting the best parents in the population for mating.
            parents = [population_text[i[0]] for i in best]
            parents_copy = copy.deepcopy(parents)
            print("Parents")
            for i in range(0, len(parents)):
                print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                                 for row in parents[i]]))
                print("")

            # Generating next generation using crossover.
            offspring_x = random.randint(1, D.GSIZE - 2)
            offspring_y = random.randint(1, D.GSIZE - 2)

            # TODO OPERATOR KRZYŻOWANIA
            offspring_crossover = crossover(parents)
            print("Crossover")
            for i in range(0, len(offspring_crossover)):
                print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                                 for row in offspring_crossover[i]]))
                print("")

            # TODO OPERATOR MUTACJI
            offspring_mutation = mutation(population_units, offspring_crossover, population_size - num_parents,
                                          num_mutations=10)
            print("Mutation")
            for i in range(0, len(offspring_mutation)):
                print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                                 for row in offspring_mutation[i]]))
                print("")

            population_text_copy = copy.deepcopy(population_text)
            unused_indexes = [i for i in range(0, population_size) if i not in [j[0] for j in best]]
            # Creating next generation
            population_text = []
            for k in parents_copy:
                population_text.append(k)
            for k in range(0, len(offspring_mutation)):
                population_text.append(offspring_mutation[k])
            while len(population_text) < population_size:
                x = random.choice(unused_indexes)
                population_text.append(population_text_copy[x])
                unused_indexes.remove(x)

            # TODO WARUNEK STOPU
            stop = 0
            if generation > 10:
                if best_outputs[-1] / best_outputs[-2] < 1.001:
                    stop += 1
                if best_outputs[-1] / best_outputs[-3] < 1.001:
                    stop += 1
                if best_outputs[-2] / best_outputs[-3] < 1.001:
                    stop += 1

    # final Fitness
    fitness = []
    for i in range(0, population_size):
        fitness.append((i, population_fitness(population_text[i], field, population_size)))

    print("Final Fitness")
    print(fitness)

    best = sorted(fitness, key=lambda tup: tup[1])[0:num_parents]

    print("Best solution : ", )
    for i in range(0, D.GSIZE):
        print(population_text[best[0][0]][i])
    print("Best solution fitness : ", best[0][1])

    pretty_printer(best_outputs)

    # TODO REALLY return best iteration of field
    return 0


if __name__ == "__main__":

    # Define the map of the field
    mapschema = maps.createField()

    # Create field array
    field = []

    # Populate the field array
    for row in range(D.GSIZE):
        field.append([])
        for column in range(D.GSIZE):
            fieldbit = F.Field(row, column, mapschema[column][row])
            field[row].append(fieldbit)

    genetic_algorithm_setup(field)
