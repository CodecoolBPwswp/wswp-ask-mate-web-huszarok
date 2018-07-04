'''Common functions to read/write/append CSV files without feature specific knowledge.
The layer that have access to any kind of long term data storage.
In this case, we use CSV files, but later on we'll change this to SQL database. So in the future, we only need to change in this layer.'''

import csv


def get_data_from_file(data):
    list_of_entries = []
    filename = "%s" % data
    with open(filename, "r") as file:
        entries = csv.DictReader(file)
        for line in entries:
            list_of_entries.append(line)
    return list_of_entries


def append_data_to_file(data, question_data):
    filename = "%s" % data
    with open(filename, "a") as file:
        writer = csv.writer(file)
        writer.writerow(question_data)


def update_data_in_file(data, updated_question_data):
    list_of_entries = []
    filename = "%s" % data
    with open(filename, "r") as file:
        entries = csv.DictReader(file)
        for line in entries:
            if line['id'] == updated_question_data['id']:
                list_of_entries.append(updated_question_data)
            else:
                list_of_entries.append(line)
    with open(filename, "w") as file:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(list_of_entries)



