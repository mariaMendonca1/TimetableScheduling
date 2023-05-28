# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

from random import choice, randint, random


def single_point_co(p1, p2):
    """ 
    To perform crossover. One point is randomly selected to perform crossover
    Parameters:
        p1(class): parent 1
        p2(class): parent 2
    Returns:
        2 objects class Individual: offspring 1 and offspring 2
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]
    return offspring1, offspring2

def uniform_co(p1, p2):
    """
    To perform crossover. Randomly selects each gene from either parent with equal probability.

    Parameters:
        p1(class): parent 1
        p2(class): parent 2
    Returns:
        2 objects class Individual: offspring 1 and offspring 2
    """
    offspring1 = []
    offspring2 = []

    for attr1, attr2 in zip(p1, p2):
        if random() < 0.5:  
            # Select attribute from parent1
            offspring1.append(attr1)
            offspring2.append(attr2)
        else:  
            # Select attribute from parent2
            offspring1.append(attr2)
            offspring2.append(attr1)

    return offspring1, offspring2

def abc(p1, p2):
    """
    Attribute-Based Crossover. Randomly selects a number of changes in attributes, 
    between 1/4 and 3/4 of all attributes. Then, it checks if the attribute to be 
    changed has not yet been changed in this iteration and performs the swap.
    Parameters:
        p1(class): parent 1
        p2(class): parent 2
    Returns:
        2 objects class Individual: offspring 1 and offspring 2
    """
    offspring1 = p1[:]
    offspring2 = p2[:]
    
    sizeInd = len(p1)
    numAtrr = len(vars(p1[0]))
    num_attribute_exchanges = randint(int((sizeInd*numAtrr) * (1/4)) - 1, (int((sizeInd*numAtrr) * (3/4)) - 1))
    n = 0

    #To save attributes that were already changed to prevent repetition
    changed_attributes = []

    # Randomly selects attributes to exchange between objects
    while n < num_attribute_exchanges:
        # Selects a random object index from the parents
        object_index = randint(0, len(p1) - 1)

        # Selects a random attribute to exchange from the objects
        attribute_to_exchange = choice(list(vars(p1[object_index]).keys())) 

        if (object_index,attribute_to_exchange) not in changed_attributes:
            changed_attributes.append((object_index,attribute_to_exchange))
            n += 1

            geneP1 = p1[object_index]
            geneP2 = p2[object_index]
            geneO1 = offspring1[object_index]
            geneO2 = offspring2[object_index]

            temp = geneP1.get_attribute(attribute_to_exchange)
            geneO1.set_attribute(attribute_to_exchange, geneP2.get_attribute(attribute_to_exchange))
            geneO2.set_attribute(attribute_to_exchange, temp)

    return offspring1, offspring2
