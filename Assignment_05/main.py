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

def process_person_name(dict):
    from functools import reduce

    #Get list of Names from Dictionary
    lst_Names = [dict[person]['name'].strip()  for person in dict.keys()]

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

    for person in dict.keys():
        try:

            if str(dict[person]['name']).strip().split(' ')[0][0].lower() == \
                    str(lst_names_filtered[intIndex]).strip().split(' ')[1][0].lower():
                dict[person]['name'] = lst_names_filtered[intIndex]
                dict[person]['Year'] = current_year - int(dict[person]['age']) -1
                dict[person]['amount_deposited'] = float(reduce(lambda x,y:x+y, dict[person]['amount_deposited']))
        except Exception:
            dict[person]['name'] = 'REMOVE'
        intIndex +=1

    return dict

def remove_invalid_item_from_dict(_dict):
    for key, value in dict(_dict).items():
        nested_dict = value
        for nestedkey, nestedvalue in dict(value).items():
            if nestedvalue == 'REMOVE':
                del _dict[key]

    return  _dict

def recursive_items(dictionary, getResultType):
    # getResultType:1 -> key only, getResultType:2 -> value only, getResultType:3 both,value
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value, getResultType)
        else:
            if getResultType == 1:
                yield (key)
            elif getResultType == 2:
                yield (value)
            else:
                yield (key, value)

def getHeaderItems(param_dict):
    distinct_headers = []
    distinct_headers.append(" ")#This is the blank item header to adjust Serial Numbers in data rows
    for key in recursive_items(param_dict, 1):
        if key not in distinct_headers:
            distinct_headers.append(key)
    return distinct_headers

def getDataRows(param_dict, param_dataHeaders):
    datarows = []
    index = 0
    for key in param_dict.keys():
        lst_row = []
        lst_row.append(index)

        for headerval in param_dataHeaders:
            if headerval != " ":
                lst_row.append(str(param_dict[key][headerval]).replace("['","").replace("']",""))

        datarows.append(lst_row)
        index += 1

    return datarows

def write_dictionary_to_file(dict, _filename,_fileformat):
    import csv

    # Creating a new dictionary
    final_dict = {}
    # adding two new elements to the dictionary
    final_dict["current_Date"] = datetime.datetime.now().strftime('%d-%b-%G')
    final_dict["Data"] = dict

    # Creating a json file with name assignment_02 and writing it to the same level of directory in which the
    # main.py exists
    # with open(_filename+'.'+_fileformat, 'w') as file:
    #     json.dump(final_dict, file, indent=2, sort_keys=True)
    # Details = ['Name', 'class', 'passoutYear', 'subject']
    headerItems = getHeaderItems(dict)
    # rows = [['sushma', '2nd', '2023', 'Physics'],
    #         ['john', '3rd', '2022', 'M2'],
    #         ['kushi', '4th', '2021', 'M4']
    #         ]
    dataRows = getDataRows(dict,headerItems)

    for i in range(0,len(headerItems)):
        # replacing the _ with space
        # make each word in the header label as Title case
        headerItems[i] = headerItems[i].replace('_', ' ').title()

    with open(_filename+'.'+_fileformat, 'w') as f:
        write = csv.writer(f)
        write.writerow(headerItems)
        write.writerows(dataRows)

def process():
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

    #changing the position of amount_deposited at the end
    #this is done removing or popping the existing node with name 'amount_deposited' and then adding aother
    #node with same name i.e. 'amount_deposited'
    for value in updated_dict.values():
        value["amout_deposited"] = value.pop('amount_deposited')

    write_dictionary_to_file(updated_dict, 'names', 'csv')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
