import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    result = []

    for test_case in data:
        result.append(test_case)
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)



