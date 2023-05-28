# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

from charles import Individual
from data import simple_data, complex_data
from tsp import get_fitness1, get_fitness2, get_fitness3, eval
from selection import tournament_sel
from crossover import single_point_co, uniform_co, abc
from mutation import single_mutation, attribute_exchange_mutation, new_gene_mutation

paramsElitism = {
    'select': [tournament_sel],
    'mutate': [single_mutation, attribute_exchange_mutation, new_gene_mutation],
    'crossover': [single_point_co, uniform_co, abc],
    'mut_prob': [0.05],
    'xo_prob': [0.9],
    'elitism': [False],
    'population': [100]
}

paramsBase = {
    'select': [tournament_sel],
    'mutate': [single_mutation, attribute_exchange_mutation, new_gene_mutation],
    'crossover': [single_point_co, uniform_co, abc],
    'mut_prob': [0.05],
    'xo_prob': [0.9],
    'elitism': [True],
    'population': [100]
}

paramsBasePopulation = {
    'select': [tournament_sel],
    'mutate': [single_mutation, attribute_exchange_mutation, new_gene_mutation],
    'crossover': [single_point_co, uniform_co, abc],
    'mut_prob': [0.05],
    'xo_prob': [0.9],
    'elitism': [True],
    'population': [200]
}

paramsBaseProbMutCross = {
    'select': [tournament_sel],
    'mutate': [single_mutation, attribute_exchange_mutation, new_gene_mutation],
    'crossover': [single_point_co, uniform_co, abc],
    'mut_prob': [0.2], # mutation rate between 0 and 0.2
    'xo_prob': [0.8],  # crossover rate between 0.8 and 1.0
    'elitism': [True],
    'population': [100]
}

paramsAllChanged = {
    'select': [tournament_sel],
    'mutate': [single_mutation, attribute_exchange_mutation, new_gene_mutation],
    'crossover': [single_point_co, uniform_co, abc],
    'mut_prob': [0.2], # mutation rate between 0 and 0.2
    'xo_prob': [0.8],  # crossover rate between 0.8 and 1.0
    'elitism': [True],
    'population': [200]
}

def timetableScheduling(nRuns, nGens, parameters, phase, improvement, data=simple_data, fitness=1):
    """
    In this function, the parameters we want to test will be passed and files will be saved with 
    the output in the desired folder
    Parameters:
        nRuns(int): number of runs to perform for each configuration
        nGens(int): number of generations to perform for each configuration
        parameters(Dictionary): parameters to use to run the configuration
        phase(str): 'None', for the case of testing the elistism True vs False;
                    'Testing', to test base parameters for each type of data 
                    (simple and complex) with each fitness function 1, 2 and 3;
                    'Improving', trying to change hyperparemeters to improve results from 'Testing'.
        improvement(str): Type of improvement 'None', for not being in this phase;
                          'Pop', improvement in the number of individuals in the Population;
                          'Prob', improvement in the probabilities of mutation and crossover;
                          'PopProbRuns', improvement in the number of individuals in the Population, 
                           probabilities of mutation and crossover and number of runs performed.
        data(Dictionary): The data used (simple data default)
        fitness(int): fitness function to use
    """
    #choosing the fitness function
    if fitness == 1:
        # Monkey patching
        Individual.get_fitness = lambda self: get_fitness1(self, data)
    elif fitness == 2:
        # Monkey patching
        Individual.get_fitness = lambda self: get_fitness2(self, data)
    elif fitness == 3:
        # Monkey patching
        Individual.get_fitness = lambda self: get_fitness3(self, data)

    #Getting the folder name where to put later the files
    localVariables = locals()
    fitnessfolder = localVariables['fitness']
    globalVariables = globals()
    datafolder = [key for key, val in globalVariables.items() if val == localVariables['data']]
    folder = str(datafolder[0]) +"_"+'fitness'+str(fitnessfolder)
    if phase == 'Testing':
        folderToStore = phase+'/'+folder
    elif phase == 'None':
        folderToStore = phase
    elif phase == 'Improving':
        folderToStore = phase+'/'+improvement+'/'+folder

    eval(nRuns, nGens, parameters, folderToStore, data)


# Check the impact of elitism in the fitness

# timetableScheduling(30, 100, paramsElitism, 'None', 'None', simple_data, fitness=1)

# Checking the performance for each type of data with each fitness function

# timetableScheduling(30, 100, paramsBase, 'Testing', 'None', simple_data, fitness=1)
# timetableScheduling(30, 100, paramsBase, 'Testing', 'None', complex_data, fitness=1)
# timetableScheduling(30, 100, paramsBase, 'Testing', 'None', simple_data, fitness=2)
# timetableScheduling(30, 100, paramsBase, 'Testing', 'None', complex_data, fitness=2)
# timetableScheduling(30, 100, paramsBase, 'Testing', 'None', simple_data, fitness=3)
# timetableScheduling(30, 100, paramsBase, 'Testing', 'None', complex_data, fitness=3)

# Trying to improve results from combination of data and fitness function, population

# timetableScheduling(30, 100, paramsBasePopulation, 'Improving', 'Pop', complex_data, fitness=1)
# timetableScheduling(30, 100, paramsBasePopulation, 'Improving', 'Pop',  complex_data, fitness=2)
# timetableScheduling(30, 100, paramsBasePopulation, 'Improving', 'Pop',  complex_data, fitness=3)

# Trying to improve results from combination of data and fitness function, mut_prob and xo_prob

# timetableScheduling(30, 100, paramsBaseProbMutCross, 'Improving', 'Prob', complex_data, fitness=1)
# timetableScheduling(30, 100, paramsBaseProbMutCross, 'Improving', 'Prob', complex_data, fitness=2)
# timetableScheduling(30, 100, paramsBaseProbMutCross, 'Improving', 'Prob', complex_data, fitness=3)

# Checking the impact of all the changes made before

# timetableScheduling(40, 100, paramsAllChanged, 'Improving', 'PopProbRuns', complex_data, fitness=1)
# timetableScheduling(40, 100, paramsAllChanged, 'Improving', 'PopProbRuns', complex_data, fitness=2)
# timetableScheduling(40, 100, paramsAllChanged, 'Improving', 'PopProbRuns', complex_data, fitness=3)