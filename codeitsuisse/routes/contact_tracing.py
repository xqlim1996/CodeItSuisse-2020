import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    result = contact_trace(data)
    # for test_case in data:
    #     result.append(contact_trace(test_case))
    

    # logging.info("My result :{}".format(infected))
    return json.dumps(result)


def contact_trace(test_case): #input is dictionary
    infected_genome = test_case['infected']['genome'].split('-')
    origin_genome = test_case['origin']['genome'].split('-')
    
    infected_name = test_case['infected']['name']
    origin_name = test_case['origin']['name']
    clusters = {}
    for cluster in test_case['cluster']:
        genome = cluster['genome'].split('-')
        clusters[cluster['name']] = genome

    clusters[origin_name] = origin_genome

    #format-> name : [[name, non_silent], [name2, non_silent2]]
    graph_map = {}
    graph_map[origin_name] = []


    #map among clusters and origin
    for name, genome in clusters.items():
        if name == origin_name:
            continue
        min_nodes = []
        for name_other, genome_other in clusters.items():
            min_diff = 99999999
            dist_dict = {} #format is name: [dist, non-silent]
            if name != name_other:
                diff_genome, non_silent = compare_genome(genome, genome_other)
                # print('clusters')
                # print(diff_genome, non_silent)
                dist_dict[name_other] = [diff_genome, non_silent]
                if diff_genome <= min_diff and diff_genome != 0:
                    min_diff = diff_genome
                    # min_nodes.append([name_other, non_silent])

        # print(dist_dict)
        for dist_name, details in dist_dict.items():
            if details[0] == min_diff:
                min_nodes.append([dist_name, details[1]])
        graph_map[name] = min_nodes

    #mapping for infected -> clusters
    infected_map = []
    dist_dict = {} #format is name: [dist, non-silent]
    min_diff = 99999999
    for name, genome in clusters.items():
        # print('name: ' + name)
        diff_genome, non_silent = compare_genome(genome, infected_genome)
        dist_dict[name] = [diff_genome, non_silent]
        # print('infected')
        # print(diff_genome, non_silent)
        if diff_genome <= min_diff:
            min_diff = diff_genome

    for name, details in dist_dict.items():
        if details[0] == min_diff:
            infected_map.append([name, details[1]])

            # infected_map.append([name, non_silent])

    graph_map[infected_name] = infected_map
    print('GRAPH:')
    print(graph_map)

    paths = []
    path_counter = len(clusters)
    #worst case is go through every cluster and origin
    next_nodes = infected_map
    for node in infected_map:
        paths.append([[infected_name], node])
        
    temp = paths.copy()
    output = []
    # print('PATH')
    # print('infected paths:' + str(paths))
    while len(temp) > 0:
        # print('temp: {}'.format(temp))
        for index in range(len(paths)):
            # print('LOOP')
            path = paths[index]
            last_node = path[-1]
            
            if type(last_node) == str: #edge case for infected
                next_nodes = graph_map[last_node]
            else:
                next_nodes = graph_map[last_node[0]]

            if len(next_nodes) == 0: #no more next node
                # print('temp removing path: ' + str(path))
                output.append(path)
                temp.remove(path)
            elif len(next_nodes) == 1:
                
                path.append(next_nodes[0])
                temp[index] = path
                # print('temp updating path: ' + str(path))
            else:
                path.append(next_nodes[0])
                for node in next_nodes[1:]:
                    new_path = path.copy()
                    new_path.append(node)
                    temp.append(new_path)
                    # print('temp adding new path' + str(new_path))
        paths = temp.copy()
        # print('paths:' + str(paths))

    #format output
    
    # print(output)
    output_format = []

    for path in output:
        path_format = ''
        for node in path:
            if len(node) == 1: #infected
                path_format += node[0]
            else:
                if node[1] == True:
                    path_format += '*'
                path_format += ' -> '
                path_format += node[0]
        output_format.append(path_format)

    print('OUTPUT')
    print(output_format)

    return output_format
                
def compare_genome(genome1, genome2):
    diff_genome = 0 #format is clusters then origin
    first_char_diff_genome = 0 #format is clusters then origin
    non_silent = False

    for index in range(len(genome1)):
        if genome1[index] != genome2[index]: #check for num diff char and if first char diff
            print('AFAS')

            genome1_instr = list(genome1[index])
            genome2_instr = list(genome2[index])

            #compare num diff in instr.
            diff_instr = compare_instr(genome1_instr, genome2_instr)
            print(diff_instr)
            diff_genome += diff_instr[0]
            first_char_diff_genome += diff_instr[1]
            # print('silent')
    if first_char_diff_genome > 1:
        non_silent = True
    
    return diff_genome, non_silent

        # if infected_genome[index] != origin_genome[index]:
        #     infect_instr = infected_genome[index].split()
        #     origin_instr = origin_genome[index].split()

        #     diff_origin = compare_instr(infect_instr, cluster_instr)
        #     diff_arr[1] += diff_origin[0]
        #     first_char_diff_arr[1] += diff_origin[1]
                
def compare_instr(instr1, instr2):
    print('instr1: ' + str(instr1))
    print('instr2: ' + str(instr2))

    diff = 0
    first_char_diff = 0
    # print(instr_1, instr_2)
    for char_index in range(len(instr1)):
        # print(instr1[char_index])
        # print(instr1[char_index])
        if instr1[char_index] != instr2[char_index]:
            if char_index == 0:
                first_char_diff += 1
            diff += 1
    
    return [diff, first_char_diff]

    
def main():
#     test = {
#     "infected": {
#         "name":"orange",
#         "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
#     },
#     "origin": {
#         "name":"turquoise",
#         "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
#     },
#     "cluster":[
#         {
#             "name":"blue",
#             "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
#         },
#         {
#             "name":"magenta",
#             "genome":"aca-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
#         }
#     ]
# }

    test = {
    "infected": {
        "name":"orange",
        "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
    },
    "origin": {
        "name":"turquoise",
        "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
    },
    "cluster":[
        {
            "name":"magenta",
            "genome":"acg-gcu-uca-gca-acu-ccc-gua-acg-gcu-uca-gca-acu-cac-gaa"
        }
    ]
}
    return(contact_trace(test))