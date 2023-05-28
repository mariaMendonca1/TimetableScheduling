# Project Timetable Scheduling Problem, CIFO
# Daniel Branco, 20220599
# Inês Ventura, 20220612
# Maria Mendonça, 20220625
# Miguel David,  20220622

#Data to be used was created by the group, two kinds, simple data 
#with less data and complex data with more data and the same number of variables

simple_data = {
    'day': ["Monday", "Tuesday", "Wednesday"],
    'timeslot' : ["10", "12", "14"],
    'subject' : ["Data Mining", "Machine Learning"],
    'group' : ["A", "B"],
    'classroom' : ["1","2"],
    'teacher' : ["Maria Mendonca", "Miguel David"],
    'classesPerSubject' : 2
}

complex_data = {
    'day' : ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    'timeslot' : ["8", "10", "12", "14", "16"],
    'subject' : ["Data Mining", "Machine Learning", "Statistics", "Programming", "Storing", "CIFO"],
    'group' : ["A", "B", "C"],
    'classroom' : ["1", "2", "3"],
    'teacher' : ["Maria Mendonca", "Miguel David", "Ines Ventura", "Daniel Branco", "Miguel Mendonca", "Ines Branco"],
    'classesPerSubject' : 2
}

