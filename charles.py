# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

from random import choice, random
from operator import attrgetter
from copy import deepcopy

class Class:
    def __init__(self, group, classroom, timeslot, day, subject, teacher):
        """
        Initiates a Class object
        Parameters:
            group(str): value of the group
            classroom(str): value of the classroom
            timeslot(str): value of the timeslot
            day(str): value of the day
            subject(str): value of the subject
            teacher(str): value of the teacher
        Returns:
            Object: Class object 
        """
        self.day = day
        self.timeslot = timeslot
        self.classroom = classroom
        self.subject = subject
        self.group = group
        self.teacher = teacher

    #Gets
    def get_attribute(self, attribute):
        """
        Check which kind of attribute to return from a Class object
        Parameters:
            attribute(str): type of attribute to return its value
        Returns:
            str: attribute value of the Class object 
        """
        if attribute == "subject":
            return self.subject
        elif attribute == "group":
            return self.group
        elif attribute == "day":
            return self.day
        elif attribute == "classroom":
            return self.classroom
        elif attribute == "timeslot":
            return self.timeslot
        elif attribute == "teacher":
            return self.teacher

    def get_group(self):
        """
        Returns:
            str: group value of the Class object  
        """
        return self.group

    def get_classroom(self):
        """
        Returns:
            str: classroom value of the Class object  
        """
        return self.classroom

    def get_timeslot(self):
        """
        Returns:
            str: timeslot value of the Class object  
        """
        return self.timeslot
    
    def get_day(self):
        """
        Returns:
            str: day value of the Class object  
        """
        return self.day

    def get_subject(self):
        """
        Returns:
            str: subject value of the Class object  
        """
        return self.subject
    
    def get_teacher(self):
        """
        Returns:
            str: teacher value of the Class object  
        """
        return self.teacher
    
    #Sets
    def set_attribute(self, attribute, new_attribute):
        """
        Check which kind of attribute to change from a Class object
        Parameters:
            attribute(str): type of attribute to change its value
            new_attribute(str): new value for the attribute
        """
        if attribute == "subject":
            self.subject = new_attribute
        elif attribute == "group":
            self.group = new_attribute
        elif attribute == "day":
            self.day = new_attribute
        elif attribute == "classroom":
            self.classroom = new_attribute
        elif attribute == "timeslot":
            self.timeslot = new_attribute
        elif attribute == "teacher":
            self.teacher = new_attribute


    def set_group(self, new_group):
        """
        Changes the group value of a Class object 
        Parameters:
            new_group(str): new value for the group attribute of the Class object 
        """
        self.group = new_group

    def set_classroom(self, new_classroom):
        """
        Changes the classroom value of a Class object 
        Parameters:
            new_classroom(str): new value for the group attribute of the Class object 
        """
        self.classroom = new_classroom

    def set_timeslot(self, new_timeslot):
        """
        Changes the timeslot value of a Class object 
        Parameters:
            new_timeslot(str): new value for the timeslot attribute of the Class object 
        """
        self.timeslot = new_timeslot
    
    def set_day(self, new_day):
        """
        Changes the day value of a Class object 
        Parameters:
            new_day(str): new value for the day attribute of the Class object 
        """
        self.day = new_day

    def set_subject(self, new_subject):
        """
        Changes the subject value of a Class object 
        Parameters:
            new_subject(str): new value for the subject attribute of the Class object 
        """
        self.subject = new_subject
    
    def set_teacher(self, new_teacher):
        """
        Changes the teacher value of a Class object 
        Parameters:
            new_teacher(str): new value for the teacher attribute of the Class object 
        """
        self.teacher = new_teacher
    
    def __len__(self):
        """
        Checks the number of attributes of the Class object
        Returns:
            int: number of all the attributes of a Class Object
        """
        #vars(self) returns a dictionary containing all the attributes and their 
        #corresponding values for the self object.
        return len(vars(self)) 

    def __repr__(self):
        """
        Returns:
            str: representation of a gene in a individual
        """
        return f"Class block: {self.get_day()}, {self.get_timeslot()}, {self.get_classroom()}, {self.get_subject()}, {self.get_group()}, {self.get_teacher()}"

class Individual:
    def __init__(
        self,
        representation=None,
        size=None,
        days=None,
        timeslots=None,
        subjects=None,
        groups=None,
        classrooms=None,
        teachers = None
    ):
        """
        Initiates a Individual object
        Parameters:
            representation(str): value of the group
            size(str): value of the size
            days(str): value of the day
            timeslots(str): value of the timeslot
            subjects(str): value of the subject
            groups(str): value of the group
            classrooms(str): value of the classroom
            teachers(str): value of the teacher
        Returns:
            Object: Individual object 
        """
        if representation == None:   
            #Creates the representation
            self.representation = []
            for i in range(size): 
                #Chooses randomly for arguments to create a Class Object
                day = choice(days)
                timeslot = choice(timeslots)
                subject = choice(subjects)
                group = choice(groups)
                classroom = choice(classrooms)
                teacher = choice(teachers)
                #Creation of the Class Object
                c = Class(group, classroom, timeslot, day, subject, teacher)  
                self.representation.append(c)

        else:
            self.representation = representation
        self.fitness = self.get_fitness()   

    def get_fitness(self):
        """
        Fitness of the individual
        """
        #Monkey Patching, acordingly to the fitness function to use
        raise Exception("You need to monkey patch the fitness path.") 

    def __len__(self):
        """
        Checks the lenght of the representation of a Individual object
        Returns:
            int: number of all the attributes of a Individual Object
        """
        return len(self.representation)

    def __getitem__(self, position):
        """
        Gets a gene from the representation of an individual at a specific position
        Returns:
            str: gene value of a Individual Object
        """
        return self.representation[position]

    def __setitem__(self, position, value):
        """
        Sets a given value of a Individual object, in a certain position
        Parameters:
            position(int): index of a gene in the Individual object to change
            value(str): new value of a gene in the Individual object
        """
        self.representation[position] = value

    def __repr__(self):
        """
        Returns:
            str: representation of a Individual
        """
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"



class Population:
    def __init__(self, size, **kwargs):
        """
        Initiates a Population object
        Parameters:
            size(int): number of individuals to constitute the Population Object
            days(str): value of the day
            subjects(str): value of the subject
            classrooms(str): value of the classroom
            groups(str): value of the group
            timeslots(str): value of the timeslot
            teachers(str): value of the teacher
        Returns:
            Object: Population object 
        """
        self.individuals = []
        self.size = size
        for i in range(size):
            self.individuals.append(
                #Creation of one individual
                Individual(                              
                    size=kwargs["sol_size"],
                    days=kwargs["days"],
                    subjects=kwargs["subjects"],
                    classrooms=kwargs["classrooms"],
                    groups=kwargs["groups"],
                    timeslots=kwargs["timeslots"],
                    teachers=kwargs["teachers"],
                )
            )

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism, data):
        """
        Iterative process by which a Population Object, that constitutes candidate 
        solutions evolves over successive generations to minimize the timetable scheduling problem.
        Parameters:
            gens(int): number of generations that the algorithm will run
            xo_prob(int): probability of crossover
            mut_prob(int): probability of mutation
            select(function): selection method to use, for parents choice
            mutate(function): mutation method to use
            crossover(function): crossover method to use
            elitism(boolean): preserve or not the best individuals in the population
            data(dictionary): type of data to use, simple or complex
        Returns:
            gen_totalFitness(list): The value of fitness for each generation
        """
        #To preserve for each generation the best fitness
        gen_totalFitness = [] 
        for i in range(gens):
            new_pop = []

            if elitism:
                #Copying the best individuals to preserve, meaning the individuals 
                #with lower fitness, because it is a minimization problem
                elite = deepcopy(min(self.individuals, key=attrgetter("fitness"))) 

            while len(new_pop) < self.size: 
                #Selection of both parents
                parent1, parent2 = select(self), select(self)

                if random() < xo_prob:
                    #Performing crossover in case the random number generated is 
                    #lower than the threshold probability to perform crossover
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if random() < mut_prob:
                    #Performing mutation in case the random number generated is 
                    #lower than the threshold probability to perform mutation
                    if (mutate.__name__ == 'new_gene_mutation') or (mutate.__name__ == 'single_mutation'):
                        #If the type of mutation to be performed is new gene mutation or single mutation
                        #it is necessary to pass as a input the data
                        offspring1 = mutate(offspring1, data)
                    else:
                        offspring1 = mutate(offspring1)

                if random() < mut_prob:
                    #The same as before, but now for the offspring2
                    if (mutate.__name__ == 'new_gene_mutation') or (mutate.__name__ == 'single_mutation'):
                        offspring2 = mutate(offspring2, data)
                    else:
                        offspring2 = mutate(offspring2)

                #Place the newly created individuals in the new population
                new_pop.append(Individual(representation=offspring1))

                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                #Checking for the worst individual in the new population, 
                #meaning the individual with higher fitness
                worst = max(new_pop, key=attrgetter("fitness"))
                if elite.fitness < worst.fitness:
                    new_pop.pop(new_pop.index(worst))
                    new_pop.append(elite)
            
            #Changing the population for the new one where was performed
            #selection, crossover and mutation
            self.individuals = new_pop
            
            print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')

            print("GEN", i)

            #Checking for each generation what is the lower fitness observed
            genFitness = float(min(self, key=attrgetter("fitness")).fitness)
            gen_totalFitness.append(genFitness)

        return gen_totalFitness 

    def __len__(self):
        """
        Checks the number of individuals of the Population object
        Returns:
            int: number of all the individuals in the Population
        """
        return len(self.individuals)

    def __getitem__(self, position):
        """
        Gets a individual from the Population Object at a specific position
        Returns:
            Individual: an Individual Object
        """
        return self.individuals[position]