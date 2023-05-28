# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

import pandas as pd
import os
from charles import Population
from data import simple_data
import matplotlib.pyplot as plt


def evaluateConfig(gens, select, mutate, crossover, mut_prob, xo_prob, elitism, pop_size=100, data=simple_data):
    """
    Creates a Population Object and performs evolution
    Parameters:
        gens(int): number of generations that the algorithm will run
        select(function): selection method to use, for parents choice
        mutate(function): mutation method to use
        crossover(function): crossover method to use
        mut_prob(int): probability of mutation
        xo_prob(int): probability of crossover
        elitism(boolean): preserve or not the best individuals in the population
        pop_size(int): dimension of the Population Object to be created
        data(dictionary): type of data to use, simple or complex
    Returns:
        Series: The value of fitness for each generation, to add later to 
        a dataframe for each run
    """
    #Creation of the Population Object
    pop = Population(
        size=pop_size, sol_size=len(data['group'])*len(data['subject'])*data['classesPerSubject'], classrooms=data['classroom'], groups=data['group'], 
        subjects=data['subject'], timeslots=data['timeslot'], days=data['day'], teachers=data['teacher']
        )
    
    #Evolution with the inputs given
    result = pop.evolve(gens=gens, select=select, mutate=mutate, crossover=crossover, mut_prob=mut_prob, xo_prob=xo_prob, elitism=elitism, data=data)
    #Creates the Series with the values for each generation performed in evolution
    fitnessRun = pd.Series(result)

    return fitnessRun


def comparisonConfig(folderToShow):
    """
    Creates a plot with each configuration, for each type of data and fitness function
    Parameters:
        folderToShow(str): folder path where to place the plot of configurations
    """
    folder_path = folderToShow
    abf_data = []
    std = []
    fileNames = []

    #Checks for each .csv file in the path provided as an input
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            #Add the name of each file found in the folder to a list
            fileNames.append(file_name)
            file_path = os.path.join(folder_path, file_name)
            #reads the csv in order to retrieve the data needed to create the plot
            df = pd.read_csv(file_path)
            #Check the column with the name 'ABF' and adds the values to the list abf_data
            abf_data.append(df['ABF']) 
            #Perform the same thing as above to the list std
            std.append(df['StdDev'])
    
    #To create the x-axis, with the number of generations       
    generations = [i for i in range(len(abf_data[0]))]

    #Creating the plot for each configuration possible
    for config in range(len(abf_data)):
        #x-axis, generations performed
        #y-axis, values of abf 
        #label, the configuration performed
        plt.plot(generations, abf_data[config], label=str(fileNames[config]).replace(".csv", ""))
        #Adding to the plot the standard deviations, in order to latter analyze the statistical significance
        plt.fill_between(generations, abf_data[config] - std[config], abf_data[config] + std[config], alpha=0.1)
    
    plt.title('ABF results for each configuration')
    plt.xlabel('Generations')
    plt.ylabel('ABF')
    plt.legend(loc='upper right')
    plt.grid(True)
    #Saving the plot in a .jpeg image in order to perserve it when the run ends
    plot = str(folderToShow).replace("Results/", "")
    namePlot = plot.replace("/", ".jpeg")
    plt.savefig(folderToShow + namePlot)
    plt.show()


