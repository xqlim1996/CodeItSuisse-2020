import logging
import json
import numpy as np
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory_management():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    results = []
    for test_case in data:
        results.append(inventory_manangement(test_case))
    logging.info("result :{}".format(results))

    return json.dumps(results)




def inventory_manangement(test_case): #input is a dict
    print(test_case)
    search_name = (test_case['searchItemName']).lower()

    items = [item.lower() for item in test_case['items']]
    
    item_dist_dict = {}

    distances_list = []

    for item_name in items:
        distance, actions = levenshteinDistanceDP(search_name, item_name)
        item_dist_dict[item_name] = [item_name, distance, actions]
        distances_list.append(distance)
    
    distances_list = sorted(distances_list)
    if len(distances_list) < 10:
        max_dist_index = len(distances_list) - 1
    else:
        max_dist_index = 9

    max_dist = distances_list[max_dist_index]

    output = []

    # print('item_dict')
    # print(item_dist_dict)

    for item, values in item_dist_dict.items():
        if values[1] <= max_dist:
            output.append(values)

    output.sort(key = lambda x: (x[1][0], x[0]))
    if len(output) > 10:
        output = output[:10]
    # print('output.sorted')
    # print(output)

    output_concat = []
    for i in output:
        word = i[2]
        word_concat = ''.join(word)
        output_concat.append(word_concat)
    print(output_concat)
    return output_concat

    # for item in output:
    #     if item[]

    # for item in output:
    #     counter = 0
    #     name = list(search_name) #list(item[0])
    #     print(item)
    #     print(name)
    #     for change in item[2]:
    #         action = change[0]
    #         index = int(change[1])
    #         replacement = change[2]
    #         if action == 'r':
    #             print('replace')
    #             name[index] = replacement
    #         elif action == '+':
    #             print('add')
    #             new_str = action + replacement
    #             name.insert(index, new_str)
    #         elif action == '-':
    #             print('removes')
    #             new_str = action + replacement
    #             name.pop(index)
    #         print(name)
                
        
    

    # print(item_dist_dict)
    
    # print(levenshteinDistanceDP(search_name, item_name))


def levenshteinDistanceDP(search_name, item_name):
    rows = len(item_name) + 1
    cols = len(search_name) + 1
    # distances = np.zeros((rows, cols))
    distances = [[[0, None]]*(cols) for i in range(rows)]
    
    
    for i in range(1, rows):
        distances[i][0] = [i, '+']

    for j in range(1, cols):
        distances[0][j] = [j, '-']

    actions = []
    
    for i in range(1, rows):
        for j in range(1, cols):
            # print(i, j)
            # print(distances[0][0])
            # if i == 0: 
            #     distances[i][j] = [j, None]    # Min. operations = j 
  
            # # If second string is empty, only option is to 
            # # remove all characters of second string 
            # elif j == 0: 
            #     distances[i][j] = [i, None]    # Min. operations = i 
  
            # If last characters are same, ignore last char 
            # and recur for remaining string 
            if item_name[i-1] == search_name[j-1]: 
                
                distances[i][j] = [distances[i-1][j-1][0], 'r']
  
            # If last character are different, consider all 
            # possibilities and find minimum 
            else:
                
                # print(distances[i][j-1][0])
                # print(distances[i-1][j][0])
                # print(distances[i-1][j-1][0])
                action_cost = min(distances[i][j-1][0],        # Insert 
                                   distances[i-1][j][0],        # Remove 
                                   distances[i-1][j-1][0])    # Replace

                # action_cost = min(possibilities)
                

                if distances[i-1][j][0] < distances[i][j-1][0] and distances[i-1][j][0] < distances[i-1][j-1][0]:
                    distances[i][j] = [1 + action_cost, '+']
                elif distances[i][j-1][0] < distances[i-1][j][0] and distances[i][j-1][0] < distances[i-1][j-1][0]:
                    distances[i][j] = [1 + action_cost, '-']
                else:
                    distances[i][j] = [1 + action_cost, 'r']
                
                # index = possibilities.index(action_cost)
                # if index == 0:
                #     actions.append(['+', i])
                # elif index == 1:
                #     actions.append(['-', i])
                # else:
                #     actions.append(['r', i])

    # printDistances(distances, len(item_name), len(search_name))
    i = rows-1
    j = cols-1

    elem = distances[i][j]
    actions = []
    # print('item name len: {}'.format(len(item_name)))
    # print('search name len: {}'.format(len(search_name)))
    
    # while (i < len(item_name) or j < len(search_name)):
    while (i > 0 or j > 0):


        # print('##############')
        # print('i: {}, j: {}'.format(i,j))

        if elem[1] == '-':
            print()
            j -= 1
            actions.append(elem[1] + search_name[j])
        elif elem[1] == '+':
            i -= 1
            # print(i)
            actions.append(elem[1] + item_name[i])
        else:
            i -= 1
            j -= 1
            # print('replace {}: {}'.format(i, item_name[i]))
            actions.append(item_name[i])

        elem = distances[i][j]
        
    actions = actions[::-1]
    # print(actions)

    
    return [distances[len(item_name)][len(search_name)], actions]

def printDistances(distances, token1Length, token2Length):
    for i in range(token1Length + 1):
        for j in range(token2Length + 1):
            print((distances[i][j]), end="  ")
        print()