import logging
import json
import numpy as np


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/pre-tick', methods=['POST'])
def evaluate_pretick():
    data = request.data
    data = data.decode('utf-8')

    data = data.split('\n')
    data_formatted = []
    data.pop()
    col_names = data.pop(0).split(',')
    for row in data:
        elems = row.split(',')
        elems_formatted = []
        for elem in elems:
            elems_formatted.append(float(elem))
        data_formatted.append(elems_formatted)
 
    # data_formatted = np.array(data_formatted)
    result = data_formatted[-1][-1]

    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input");
    # result = 100
    # logging.info("My result :{}".format(result))

    return json.dumps(result);



