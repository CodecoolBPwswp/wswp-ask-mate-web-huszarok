'''Helper functions which can be called from any other layer. (but mainly from the business logic layer)'''
import data_manager


def generate_id(type):
    if type == 'question':
        list_of_entries = data_manager.get_questions_from_file()
    elif type == 'answer':
        list_of_entries = data_manager.get_answers_from_file()

    maximum_id = 0
    for entry in list_of_entries:
        if int(entry['id']) > int(maximum_id):
            maximum_id = int(entry['id'])
    maximum_id += 1
    return maximum_id
