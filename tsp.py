# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

import pandas as pd
from data import simple_data
from sklearn.model_selection import ParameterGrid
from evaluation import evaluateConfig, comparisonConfig

def get_fitness1(self, data=simple_data):
    """
    First fitness function, the simplest one, where it will be check for conflits when:
        - A classroom was simultaneously occupied by two different lectures.
        - A group had overlapping lectures, attending two different classes at the same time.
        - A group had the same lecture scheduled twice in a day.
        - A group had an incorrect number of lectures per subject per week, either less or more than the two required.
    Parameters:
        data(Dictionary): The data used
    Returns:
        conflicts(int): number of conflits found
    """
    conflicts = 0
    countPairSC = {(class_name, subject): 0 for subject in data['subject'] for class_name in data['group']}

    for i in range(len(self.representation)):
        for j in range(i + 1, len(self.representation)):
            #Check if a group had overlapping lectures, attending two different classes at the same time
            if self.representation[i].get_group() == self.representation[j].get_group() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                conflicts += 1
            #Check if a classroom was simultaneously occupied by two different lectures.
            if self.representation[i].get_classroom() == self.representation[j].get_classroom() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                conflicts += 1

            #Check if a group had the same lecture scheduled twice in a day
            if self.representation[i].get_group() == self.representation[j].get_group() and self.representation[i].get_day() == self.representation[j].get_day() and self.representation[i].get_subject() == self.representation[j].get_subject():
                conflicts += 1

        #Check if a group had an incorrect number of lectures per subject per week
        if (self.representation[i].get_group(), self.representation[i].get_subject()) in list(countPairSC.keys()):
            countPairSC[(self.representation[i].get_group(), self.representation[i].get_subject())] += 1

    conflicts += len(list(countPairSC.values())) - list(countPairSC.values()).count(data['classesPerSubject'])

    return conflicts


def get_fitness2(self, data=simple_data):
    """
    Second fitness function, a more complex one than the first, where it will be check all the conflicts on fitness1 and also the following:
        - A timetable does not have at least one free day.
        - Within a single day, a group is required to change classrooms for different lectures.
        - The schedule for each day exceeds the maximum number of classes permitted per day.
    Parameters:
        data(Dictionary): The data used
    Returns:
        conflicts(int): number of conflits found
    """
    conflicts = 0

    countPairSC = {(group_name, subject): 0 for subject in data['subject'] for group_name in data['group']}
    countPairGT = {(group_name, day): 0 for day in data['day'] for group_name in data['group']}
    countPairG = {group_name: [] for group_name in data['group']}
    countPairGCD = {(group_name, day): [] for day in data['day'] for group_name in data['group']}


    for i in range(len(self.representation)):
        duplicated1 = False
        duplicated2 = False
        duplicated3 = False
        for j in range(i + 1, len(self.representation)):
            
            #Check if a group had overlapping lectures, attending two different classes at the same time
            if self.representation[i].get_group() == self.representation[j].get_group() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                if duplicated1 == False:
                    conflicts += 1
                    duplicated1 = True
            #Check if a classroom was simultaneously occupied by two different lectures.
            if self.representation[i].get_classroom() == self.representation[j].get_classroom() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                if duplicated2 == False:
                    conflicts += 1
                    duplicated2 = True

            #Check if a group had the same lecture scheduled twice in a day
            if self.representation[i].get_group() == self.representation[j].get_group() and self.representation[i].get_day() == self.representation[j].get_day() and self.representation[i].get_subject() == self.representation[j].get_subject():
                if duplicated3 == False:
                    conflicts += 1
                    duplicated3 = True   

        #How many lectures per subject a group had in week
        if (self.representation[i].get_group(), self.representation[i].get_subject()) in list(countPairSC.keys()):
            countPairSC[(self.representation[i].get_group(), self.representation[i].get_subject())] += 1
        
        #How many classes a group had in a day
        if (self.representation[i].get_group(), self.representation[i].get_day()) in list(countPairGT.keys()):
            countPairGT[(self.representation[i].get_group(), self.representation[i].get_day())] += 1

        #Check how many days a group has classes
        if (self.representation[i].get_group()) in list(countPairG.keys()):
            value = countPairG[self.representation[i].get_group()]
            if self.representation[i].get_day() not in value:
                countPairG[self.representation[i].get_group()].append(self.representation[i].get_day())
        
        #Check how many classrooms a group has in each day
        if (self.representation[i].get_group(), self.representation[i].get_day()) in list(countPairGCD.keys()):
            value = countPairGCD[(self.representation[i].get_group(), self.representation[i].get_day())]
            if self.representation[i].get_classroom() not in value:
                countPairGCD[(self.representation[i].get_group(), self.representation[i].get_day())].append(self.representation[i].get_classroom())

    #Check if a group had an incorrect number of lectures per subject per week
    conflicts += len(list(countPairSC.values())) - list(countPairSC.values()).count(data['classesPerSubject'])

    #Check if each group has 3 classes per day
    for i in countPairGT.values():
        if i > 3:
            conflicts += 1

    #Check if a group does not have at least 1 free day
    for value_list in countPairG.values():
        if len(value_list) > (len(data['day']) - 1):
            conflicts += 1
    
    #Check if a group changes classrooms on the same day
    for value_list in countPairGCD.values():
        if len(value_list) > 1:
            conflicts += 1
    
    return conflicts


def get_fitness3(self, data=simple_data):
    """
    Last fitness function, the most complex one, takes into account all the conflicts mentioned in fitness1 and 2 but
    with the introduction of professors to our data, creates a new set of constraints for this aditional variable,
    which are:
        - Each teacher is limited to a maximum of three classes per day.
        - A professor cannot simultaneously teach two lectures.
        - A professor is associated with a specific subject, representing his/her/their area of expertise.
          Consequently, whenever a professor is assigned to teach other lectures, a conflict should be considered.
    Parameters:
        data(Dictionary): The data used
    Returns:
        conflicts(int): number of conflits found
    """
    conflicts = 0

    countPairSC = {(group_name, subject): 0 for subject in data['subject'] for group_name in data['group']}
    countPairGT = {(group_name, day): 0 for day in data['day'] for group_name in data['group']}
    countPairG = {group_name: [] for group_name in data['group']}
    countPairGCD = {(group_name, day): [] for day in data['day'] for group_name in data['group']}
    countPairTD = {(t, d): 0 for t in data['teacher'] for d in data['day']}
    subjectTeacher = {}
    for subject, teacher in zip(data['subject'], data['teacher']):
        subjectTeacher[subject] = teacher


    for i in range(len(self.representation)):
        duplicated1 = False
        duplicated2 = False
        duplicated3 = False
        duplicated4 = False
        for j in range(i + 1, len(self.representation)):
            #Check if a group had overlapping lectures, attending two different classes at the same time
            if self.representation[i].get_group() == self.representation[j].get_group() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                if duplicated1 == False:
                    conflicts += 1
                    duplicated1 = True
            #Check if a classroom was simultaneously occupied by two different lectures.
            if self.representation[i].get_classroom() == self.representation[j].get_classroom() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                if duplicated2 == False:
                    conflicts += 1
                    duplicated2 = True

            #Check if a group had the same lecture scheduled twice in a day
            if self.representation[i].get_group() == self.representation[j].get_group() and self.representation[i].get_day() == self.representation[j].get_day() and self.representation[i].get_subject() == self.representation[j].get_subject():
                if duplicated3 == False:
                    conflicts += 1
                    duplicated3 = True
            #Check if a professor is simultaneously teaching two lectures.
            if self.representation[i].get_teacher() == self.representation[j].get_teacher() and self.representation[i].get_timeslot() == self.representation[j].get_timeslot() and self.representation[i].get_day() == self.representation[j].get_day():
                if duplicated4 == False:
                    conflicts += 1
                    duplicated4 = True

        #Check if professor is teaching the designated subjects
        teacherToCheck = subjectTeacher[self.representation[i].get_subject()]
        if teacherToCheck != self.representation[i].get_teacher():
            conflicts +=1
           

        #How many lectures per subject a group had in week
        if (self.representation[i].get_group(), self.representation[i].get_subject()) in list(countPairSC.keys()):
            countPairSC[(self.representation[i].get_group(), self.representation[i].get_subject())] += 1
        
        #How many classes a group had in a day
        if (self.representation[i].get_group(), self.representation[i].get_day()) in list(countPairGT.keys()):
            countPairGT[(self.representation[i].get_group(), self.representation[i].get_day())] += 1

        #Check how many days a group has classes
        if (self.representation[i].get_group()) in list(countPairG.keys()):
            value = countPairG[self.representation[i].get_group()]
            if self.representation[i].get_day() not in value:
                countPairG[self.representation[i].get_group()].append(self.representation[i].get_day())
        
        #Check how many classrooms a group has in each day
        if (self.representation[i].get_group(), self.representation[i].get_day()) in list(countPairGCD.keys()):
            value = countPairGCD[(self.representation[i].get_group(), self.representation[i].get_day())]
            if self.representation[i].get_classroom() not in value:
                countPairGCD[(self.representation[i].get_group(), self.representation[i].get_day())].append(self.representation[i].get_classroom())

        #Check how many classes each professor has each day
        if (self.representation[i].get_teacher(), self.representation[i].get_day()) in list(countPairTD.keys()):
            countPairTD[(self.representation[i].get_teacher(), self.representation[i].get_day())] += 1

    #Check if a group had an incorrect number of lectures per subject per week
    conflicts += len(list(countPairSC.values())) - list(countPairSC.values()).count(data['classesPerSubject'])

    #Check if each group has 3 classes per day
    for i in countPairGT.values():
        if i > 3:
            conflicts += 1

    #Check if a group does not have at least 1 free day
    for value_list in countPairG.values():
        if len(value_list) > (len(data['day']) - 1):
            conflicts += 1
    
    #Check if a group changes classrooms on the same day
    for value_list in countPairGCD.values():
        if len(value_list) > 1:
            conflicts += 1

    #Check if professors have more than 3 classes per day
    for i in countPairTD.values():
        if i > 3:
            conflicts += 1

    return conflicts



def eval(nRuns, nGens, configDict, folderToStore, data=simple_data):
    """
    Eval runs the genetic algorithm and then calculates some values that will be used to make the plots
    """
    """
    Runs the genetic algorithm and then calculates some values that will be used to make the plots
    Parameters:
        nRuns(int): number of runs that the algorithm will run
        nGens(int): number of generations that the algorithm will run
        configDict(dictionary): parameters to choose to make possible configurations
        folderToStore(str): folder where to store the .csv file
        data(dictionary): type of data to use, simple or complex
    """
    #ParameterGrid, generates a grid of hyperparameter combinations for parameter tuning
    parameters = list(ParameterGrid(configDict)) 
    nConfigs = len(parameters)

    #Run the genetic algorithm with the current parameter combination
    for param_combination in range(nConfigs):
        select = parameters[param_combination]['select']
        mutate = parameters[param_combination]['mutate']
        crossover = parameters[param_combination]['crossover']
        mut_prob = parameters[param_combination]['mut_prob']
        xo_prob = parameters[param_combination]['xo_prob']
        elitism = parameters[param_combination]['elitism']
        pop_size = parameters[param_combination]['population']

        print("The configuration to be tested is: ", parameters[param_combination])
        #For each configuration creates a dataframe
        config = pd.DataFrame()
        #Adds a Series with the number of the generation
        config['Generations'] = pd.Series([i for i in range(nGens)])
        for r in range(nRuns):
            print(".............................")
            print("RUN", r)
            runs = evaluateConfig(nGens, select, mutate, crossover, mut_prob, xo_prob, elitism, pop_size, data)
            #Adds the Series from the output of the evaluateConfig function to the dataframe with the number of the run
            config['Run'+str(r)] = runs

        #Calculate the row-wise average
        config['ABF'] = round(config.iloc[:, 1:].mean(axis=1),3)
        #Calculate the row-wise standard deviation
        config['StdDev'] = round(config.iloc[:, 1:].std(axis=1),3)
        
        #Export the dataframe to a CSV file
        #In the case the substring 'None' is in the folder path provided is the evaluation of the impact of elistism 
        #to True vs False
        if 'None' in folderToStore:
            folder = 'Results/MutationFalse/'
            config.to_csv(folder+str(mutate.__name__)+'-'+str(crossover.__name__)+'.csv', index=False)
        else:
            folder = 'Results/'+folderToStore+'/'
            
            #In the case the substring 'Testing' is in the folder path provided is the phase of testing the base parameters
            if 'Testing' in folder:
                config.to_csv(folder+str(mutate.__name__)+'-'+str(crossover.__name__)+'.csv', index=False)
            
            #In the case the substring 'Improving' is in the folder path provided is the phase of improving the base parameters
            #in order to obtain better results
            elif 'Improving' in folder:
                
                #The improving is in the number of population individuals
                if 'Pop' in folder:
                    config.to_csv(folder+str(mutate.__name__)+'-'+str(crossover.__name__)+'-'+str(pop_size)+'.csv', index=False)
                
                #The improving is in the probabilities of crossover and mutation
                elif 'Prob' in folder:
                    config.to_csv(folder+str(mutate.__name__)+'-'+str(crossover.__name__)+'-'+str('prob_mut_xo')+'.csv', index=False)
                
                #The improving is in the number of population individuals, probabilities of crossover and mutation and number of runs
                elif 'PopProbRuns' in folder:
                    config.to_csv(folder+str(mutate.__name__)+'-'+str(crossover.__name__)+'-'+str('PopProbRuns')+'.csv', index=False)

    #Comparison of configurations in plot
    comparisonConfig(folder)

