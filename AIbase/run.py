from flask import Flask, abort, request
from utilities.settings import Settings
from BayesClassifierCore import BayesClassifierCore

import json
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/chatter', methods=[Settings.get_reciever_method()])
def chatter():
    if not request.json:
        abort(400)

    incoming = request.json
    if incoming['message']['type'] == 'text':
        if len(incoming['message']['content']) > 1:
            incoming['message']['content'] = BayesClassifierCore.answer(incoming['message']['content'])
        else:
            incoming['message']['content'] = Settings.get_default_unknown_text()
    elif incoming['message']['type'] == 'btn':
        abort(400)

    return json.dumps(incoming)


if __name__ == '__main__':
    app.run(host='0.0.0.0')