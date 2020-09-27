import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluate_supermarket():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    test = data.get("tests")
    result = {}
    result["answers"] = {}
    for key,value in test.items():
        result["answers"][key] = supermarket(value)
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def supermarket(test_case):

    maze = test_case['maze']
    start = test_case['start']
    end = test_case['end']

    end_row = end[1]
    end_col = end[0]

    curr_row = start[1]
    curr_col = start[0]

    #row = row no. , col = col no.

    queue = []
    queue.append([curr_row, curr_col, 1])
    counter = 1

    visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    visited[curr_row][curr_col] = True
    

    while queue:
        [curr_row, curr_col, counter] = queue.pop()
        visited[curr_row][curr_col] = True
        
        # print('curr_row, curr_col: {}'.format([curr_row, curr_col, counter]))
        
        if counter >= len(maze) * len(maze[0]):
            break

        if curr_row < 0 or curr_row > len(maze) or curr_col < 0 or curr_col > len(maze[0]):
            continue

        if [curr_row, curr_col] == [end_row, end_col]:
            # print('end: count: {}'.format(counter))
            return counter

        

        left = [curr_row, curr_col - 1]
        right = [curr_row, curr_col + 1]
        up = [curr_row - 1, curr_col]
        down = [curr_row + 1, curr_col]

        directions = [left, right, up, down]
        # print('directions: {}'.format(directions))

        for direction in directions:
            row = direction[0]
            col = direction[1]
            if row < 0 or row > len(maze) or col < 0 or col > len(maze[0]):
                continue
            
            # print('direction: {}, {}, {}'.format([row,col], maze[row][col], visited[row][row]))
            
            if maze[row][col] == 0 and visited[row][col] == False:
                # print('appending: {},{}'.format(row, col))
                queue.append([row, col, counter+1])
                visited[row][col] = True
        counter += 1
        # print(queue)

    return -1

        


