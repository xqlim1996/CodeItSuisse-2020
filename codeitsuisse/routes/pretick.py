import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/pre-tick', methods=['POST'])
def evaluate_pretick():
    data = request.datas
    # data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input");
    result = 100
    # logging.info("My result :{}".format(result))

    return json.dumps(result);



