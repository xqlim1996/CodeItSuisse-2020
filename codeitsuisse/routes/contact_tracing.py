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

    for name, genome in clusters.items():
        if name == origin_name:
            continue
        min_nodes = []
        min_diff = 99999999
        dist_dict = {} #format is name: [dist, non-silent]
        for name_other, genome_other in clusters.items():
            
            if name != name_other:
                diff_genome, non_silent = compare_genome(genome, genome_other)
                dist_dict[name_other] = [diff_genome, non_silent]
                if diff_genome <= min_diff and diff_genome != 0:
                    min_diff = diff_genome

        for dist_name, details in dist_dict.items():
            if details[0] == min_diff:
                min_nodes.append([dist_name, details[1]])
        graph_map[name] = min_nodes


    #mapping for infected -> clusters
    infected_map = []
    dist_dict = {} #format is name: [dist, non-silent]
    min_diff = 99999999
    for name, genome in clusters.items():
        diff_genome, non_silent = compare_genome(genome, infected_genome)
        dist_dict[name] = [diff_genome, non_silent]
        if diff_genome <= min_diff:
            min_diff = diff_genome

    for name, details in dist_dict.items():
        if details[0] == min_diff:
            infected_map.append([name, details[1]])


    graph_map[infected_name] = infected_map
    paths = []
    path_counter = len(clusters)
    #worst case is go through every cluster and origin
    next_nodes = infected_map
    for node in infected_map:
        paths.append([[infected_name], node])
        
    temp = paths.copy()
    output = []

    while len(temp) > 0:
        for index in range(len(paths)):
            path = paths[index]
            last_node = path[-1]
            
            if type(last_node) == str: #edge case for infected
                next_nodes = graph_map[last_node]
            else:
                next_nodes = graph_map[last_node[0]]

            if len(next_nodes) == 0: #no more next node
                output.append(path)
                temp.remove(path)
            elif len(next_nodes) == 1:
                
                path.append(next_nodes[0])
                temp[index] = path

            else:
                path.append(next_nodes[0])
                for node in next_nodes[1:]:
                    new_path = path.copy()
                    new_path.append(node)
                    temp.append(new_path)

        paths = temp.copy()


    #format output
    
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

    return output_format
                
def compare_genome(genome1, genome2):
    diff_genome = 0 #format is clusters then origin
    first_char_diff_genome = 0 #format is clusters then origin
    non_silent = False

    for index in range(len(genome1)):
        if genome1[index] != genome2[index]: #check for num diff char and if first char diff

            genome1_instr = list(genome1[index])
            genome2_instr = list(genome2[index])

            #compare num diff in instr.
            diff_instr = compare_instr(genome1_instr, genome2_instr)
            diff_genome += diff_instr[0]
            first_char_diff_genome += diff_instr[1]
    if first_char_diff_genome > 1:
        non_silent = True
    
    return diff_genome, non_silent


                
def compare_instr(instr1, instr2):

    diff = 0
    first_char_diff = 0

    for char_index in range(len(instr1)):
        
        if instr1[char_index] != instr2[char_index]:
            if char_index == 0:
                first_char_diff += 1
            diff += 1
    
    return [diff, first_char_diff]

    