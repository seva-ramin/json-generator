from flask import Flask, request, jsonify
from waitress import serve
from randjson import Driver
import random, json

import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app = Flask(__name__)
templates = {}


@app.route('/', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def index():
    return 'You shall prevail!'


@app.route('/template/<int:template_id>', defaults={'count': 1}, methods=['GET', 'POST'])
@app.route('/template/<int:template_id>/<int:count>', methods=['GET', 'POST'])
def get_handler(template_id, count):

    if template_id in templates:
        driver = templates[template_id]
    else:
        return 'Invalid Template!'

    return json.dumps(driver.get(count))


@app.route('/template', methods=['POST'])
def post_handler():
    if not request.json:
        return 'Missing template in post body'

    driver = Driver(json.dumps(request.json))
    template_id = random.randint(100000, 999999)
    while template_id in templates:
        template_id = random.randint(100000, 999999)
    templates[template_id] = driver
    response = {
        'status': 'success',
        'links': [
            {"rel": "1", "href": "/template/{}".format(template_id)},
            {"rel": "5", "href": "/template/{}/5".format(template_id)},
            {"rel": "25", "href": "/template/{}/25".format(template_id)},
        ]
    }
    return response


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
