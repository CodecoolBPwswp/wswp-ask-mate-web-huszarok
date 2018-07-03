'''Common functions to read/write/append CSV files without feature specific knowledge.
The layer that have access to any kind of long term data storage.
In this case, we use CSV files, but later on we'll change this to SQL database. So in the future, we only need to change in this layer.'''

import csv

#using CSV Reader, not Dictreader
def get_data_from_file(data):
    list_of_questions = []
    filename = "%s" % data
    with open(filename, "r") as file:
        questions = csv.DictReader(file)
        for line in questions:
            list_of_questions.append(line)
    return list_of_questions



