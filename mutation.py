# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

from random import choice, randint, sample
from charles import Class
from data import simple_data


def single_mutation(individual, data=simple_data):
    """
    Performs a single mutation on an individual.
    Parameters:
        individual(Individual): The individual to mutate.
        data(Dictionary): The data used for mutation
    Returns:
        The mutated individual. 
    """
    #Select random class and attribute index to mutate
    mut_index_class = randint(0, len(individual) - 1)
    mut_index_attr = randint(0, len(individual[0]) - 1)

    #Get a list of attributes for the selected class
    listAttr = list(vars(individual[mut_index_class]).keys())

    #From the list, select an attribute to change
    attrToChange = listAttr[mut_index_attr]

    #Select a random value for the attribute
    attr = choice(data[attrToChange])

    #Ensure the attributes are different
    while attr == individual[mut_index_class].get_attribute(attrToChange):
        #If the value is the same, select a new random value
        attr = choice(data[attrToChange])

    #Set the new attribute value
    individual[mut_index_class].set_attribute(attrToChange, attr)

    return individual

def attribute_exchange_mutation(individual):
    """
    Performs an attribute exchange mutation on an individual.
    Parameters:
        individual(Individual): The individual to mutate.
    Returns:
        The mutated individual.
    """
    #Select two random class indexes to mutate
    mut_indexes_class = sample(range(len(individual)), 2)

    #Get both classes to exchange attributes
    g01 = individual[mut_indexes_class[0]]
    g02 = individual[mut_indexes_class[1]]

    #Get the attributes of the first class
    attr1 = vars(g01)

    num_attributes = len(attr1)
    
    #Select half of the attributes from  for exchange
    attributes_to_exchange = sample(attr1.keys(), num_attributes // 2)

    #Exchange the attributes between both classes
    for attribute in attributes_to_exchange:
        #Temporarily store the attribute value of the first class
        temp = g01.get_attribute(attribute)
        g01.set_attribute(attribute, g02.get_attribute(attribute))
        g02.set_attribute(attribute, temp)

    return individual

def new_gene_mutation(individual, data=simple_data):
    """
    Performs a new gene mutation on an individual.
    Parameters:
        individual(individual): The individual to mutate.
        data(Dictionary): The data used for mutation (default: simple_data).
    Returns:
        The mutated individual.
    """
    #Select a random class index to mutate
    mut_index_class = randint(0, len(individual) - 1)

    #Randomly select each attribute
    random_day = choice(data['day'])
    random_timeslot = choice(data['timeslot'])
    random_subject = choice(data['subject'])
    random_group = choice(data['group'])
    random_classroom = choice(data['classroom'])
    random_teacher = choice(data['teacher'])

    # Create a new class with random attributes and replace the existing in a random index
    individual[mut_index_class] = Class(day=random_day, timeslot=random_timeslot, subject=random_subject,
                                        group=random_group, classroom=random_classroom, teacher=random_teacher)
    return individual