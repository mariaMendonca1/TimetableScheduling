# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

from operator import attrgetter
from random import uniform, choice

def fps(population):
    """
    To select an individual. The probability of each individual to be 
    chosen is proportionate to its fitness value
    Parameters:
        population(class): population of individuals
    Returns:
        individual(Individual): selected
    """
    #We did this 1/i.fitness because our problem is a minimization 
    #and added 0.1 in case we got a fitness = 0
    total_fitness = 0

    for i in population:
        if i.fitness == 0:
            total_fitness += 1/0.1
        else:
            total_fitness += 1/i.fitness
    
    spin = uniform(0, total_fitness)
    position = 0
    

    for individual in population:
        if individual.fitness == 0:
            position += 1/0.1
        else:
            position += 1/individual.fitness
        if position > spin:
            return individual


def tournament_sel(population, size=4):
    """
    To select an individual. The individuals within the tournament 
    compete against each other, and the one with the highest fitness is selected
    Parameters:
        population(class): population of individuals
        size(int): number of individuals competing in a torunament
    Returns:
        individual(Individual): selected
    """
    tournament = [choice(population.individuals) for _ in range(size)]
    return min(tournament, key=attrgetter("fitness"))

def ranking_sel(population):
    """
    To select an individual. It assigns a rank to each individual based on their fitness, with higher ranks indicating better fitness. 
    Probability of being chosen is dependent on that ranking.
    Parameters:
        population(class): population of individuals
    Returns:
        individual(Individual): selected
    """
    dict = {individual: individual.fitness for individual in population}

    sorted_dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}

    denominator = 0
    position = 0

    for i in range(len(population)):
        denominator += i + 1

    spin = uniform(0, 1)

    list_individuals = [x for x in sorted_dict.keys()]

    for x in range(len(list_individuals)):
        position += (x + 1) / denominator
        if position > spin:
            return list_individuals[x]