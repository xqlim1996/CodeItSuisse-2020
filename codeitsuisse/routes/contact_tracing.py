import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    data_dict = data.loads(x)


    
    logging.info("My result :{}".format(data_dict))
    return json.dumps(result)



