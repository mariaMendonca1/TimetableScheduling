from data import classes,classrooms,timeslots,days,subjects,classesPerSubject
from random import sample,choice

size = len(classes)*len(subjects)*classesPerSubject
timetable_matrix = []
timetable = []
pop_size = 1
for n in range(pop_size):
    for i in range(size):
        individual = [choice(classes),choice(classrooms),choice(timeslots),choice(days),choice(subjects)]
        timetable.append(individual)
    timetable_matrix.append(timetable)


#print(chromosome)

# get the number of rows and columns in the matrix
num_rows = len(timetable)
num_cols = len(timetable[0])

# iterate over the rows and columns and print each element
for i in range(num_rows):
    for j in range(num_cols):
        print(timetable[i][j], end=' ')
    print()  # print a new line after each row

#print(timetable_matrix)

#par turma disciplina
countPairSC = {(class_name, subject): 0 for subject in subjects for class_name in classes}

# Print the resulting dictionary
#print(countPairSC)


def get_fitness(chromosome):
    conflicts = 0
    classesPWeek = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            # ver aulas que nao podem ser sobrepostas
            if chromosome[i][0] == chromosome[j][0] and chromosome[i][2] == chromosome[j][2] and chromosome[i][3] == chromosome[j][3]:
                conflicts += 1
            #sala so pode ter uma aula de cada vez
            if chromosome[i][1] == chromosome[j][1] and chromosome[i][2] == chromosome[j][2] and chromosome[i][3] == chromosome[j][3]:
                conflicts += 1

            #ver se so ha um bloco de disciplina por dia
            if chromosome[i][0] == chromosome[j][0] and chromosome[i][3] == chromosome[j][3] and chromosome[i][4] == chromosome[j][4]:
                conflicts += 1

        # ver se cada disciplina tem as vezes pretendidas de aulas por semana
        if (chromosome[i][0], chromosome[i][4]) in list(countPairSC.keys()):
            countPairSC[(chromosome[i][0], chromosome[i][4])] += 1


    conflicts += len(list(countPairSC.values())) - list(countPairSC.values()).count(classesPerSubject)

    #print("Estes sao os valores " , len(list(countPairSC.values())))
    #print("este tem o count   ", list(countPairSC.values()).count(2))

    return conflicts

#print(get_fitness(timetable))


def matrix_maker(m_size):
    size = len(classes) * len(subjects) * classesPerSubject
    timetable_matrix = []

    for n in range(m_size):
        timetable = []
        for i in range(size):
            block = [choice(classes), choice(classrooms), choice(timeslots), choice(days), choice(subjects)]
            timetable.append(block)
        timetable_matrix.append(timetable)


    return timetable_matrix

test = matrix_maker(4)


num_rows_m = len(test)
num_cols_m = len(test[0])

for i in range(num_rows_m):
    for j in range(num_cols_m):
        for sub_list in test[i][j]:
            print(sub_list, end=' ')
        print(end='\t')
    print()
