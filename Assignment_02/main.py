from datetime import date
import datetime

def get_alphabet_excluding_chars(tpl_chars):
    #method below is called list comprehension
    alphabets = [chr(i)  for i in range(97, 123) if i not in tpl_chars]
    return tuple(alphabets)

def get_alphabet_between(_fromChar, _toChar):
    #method below is called list comprehension
    alphabets = [chr(i)  for i in range(_fromChar, _toChar) ]
    return tuple(alphabets)

def get_persons(dict):
    persons = dict.keys()
    return persons

def get_Names(dict):
    lst_persons = get_persons(dict)
    lst_Names = []

    for person in lst_persons:
        lst_Names.append(dict[person]['name'].strip())
    return lst_Names

def process_person_name(dict):
    from functools import reduce

    #Get the list of persons in the dictionary
    lst_persons = get_persons(dict)

    #Get list of Names from Dictionary
    lst_Names = get_Names(dict)

    #Cocatenate either Mr. or Ms. with each Name depending upon starting character of Name
    #if Start character is a-g then concatenate Mr. or Ms. otherwise
    func_concatenate = lambda x: \
        'Mr. ' + x if str(x).lower().startswith(get_alphabet_between(97, 104)) \
        else 'Ms. ' + x
    lst_Names_concatenated = list(map(func_concatenate, lst_Names))

    #Filter the names of the persons as per provided condition
    #condition is that remove the person data if his/her name starts with ’s’,’m’ or ‘k’
    tpl_characters = (107, 109, 115)  # 'k','m','s'
    func_filter = lambda x:str(x.split(' ')[1])[0].lower().startswith(get_alphabet_excluding_chars(tpl_characters))
    lst_names_filtered = list(filter(func_filter, lst_Names_concatenated))

    #Update the Names of persons in the dictionary
    intIndex = 0
    current_year = date.today().year

    for person in lst_persons:
        try:
            str_person_Name = person
            if str(dict[person]['name']).strip().split(' ')[0][0].lower() == \
                    str(lst_names_filtered[intIndex]).strip().split(' ')[1][0].lower():
                dict[person]['name'] = lst_names_filtered[intIndex]
                dict[person]['Year'] = current_year - int(dict[person]['age']) -1
                # print(dict[person]['amount_deposited'])
                # print(reduce(lambda x,y:x+y, dict[person]['amount_deposited']))
                dict[person]['amount_deposited'] = reduce(lambda x,y:x+y, dict[person]['amount_deposited'])
        except Exception:
            # ret_Dict.pop(str_person_Name)
            # del ret_Dict[str_person_Name]
            dict[person]['name'] = 'REMOVE'
        intIndex +=1

    return dict

def remove_invalid_item_from_dict(_dict):
    for key, value in dict(_dict).items():
        nested_dict = value
        for nestedkey, nestedvalue in dict(value).items():
            # print(nestedvalue)
            if nestedvalue == 'REMOVE':
                del _dict[key]

    return  _dict

def write_dictionary_to_file(dict, _filename,_fileformat):
    import json
    # Creating a new dictionary
    final_dict = {}
    # adding two new elements to the dictionary
    final_dict["current_Date"] = datetime.datetime.now().strftime('%d-%b-%G')
    final_dict["Data"] = dict

    # Creating a json file with name assignment_02 and writing it to the same level of directory in which the
    # main.py exists
    with open(_filename+'.'+_fileformat, 'w') as file:
        json.dump(final_dict, file, indent=2, sort_keys=True)

def process():

    # Use a breakpoint in the code line below to debug your script.
    My_Dict = {
        'person_1': {'name': ' Abdul Rafay', 'age': 22, 'Interests': ['football,cricket'],
                     'amount_deposited': [24000, 26000]},
        'person_2': {'name': 'Nancy James', 'age': 23, 'Interests': ['baseball,cricket'],
                     'amount_deposited': [24000, 27000]},
        'person_3': {'name': 'Selena Gomez', 'age': 26, 'Interests': ['baseball,table tennis'],
                     'amount_deposited': [24000, 28000]}
    }

    updated_dict = process_person_name(My_Dict)
    updated_dict = remove_invalid_item_from_dict(updated_dict)

    write_dictionary_to_file(updated_dict, 'names', 'json')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
