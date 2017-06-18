from flask import Flask, abort, request
from utilities.settings import Settings
from BayesClassifierCore import BayesClassifierCore

import json
import time
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    :return: index
    """
    return 'Hello World!'


@app.route('/chatter', methods=[Settings.get_reciever_method()])
def chatter():
    """
    Message хүлээж аваад хариу өгөх хаяг
    :return:
    """
    if Settings.get_reciever_format() == 'json':
        if not request.json:
            abort(400)
        start_time = int(round(time.time() * 1000))
        incoming = request.json
        if incoming['message']['type'] == 'text':
            if len(incoming['message']['content']) > 1:
                incoming['message']['content'] = BayesClassifierCore.answer(incoming['message']['content'])
            else:
                incoming['message']['content'] = Settings.get_default_unknown_text()
        elif incoming['message']['type'] == 'btn':
            abort(400)
        end_time = int(round(time.time() * 1000))
        incoming['message']['time'] = str(end_time - start_time)
        return json.dumps(incoming)
    elif Settings.get_reciever_format() == 'xml':
        return
    elif Settings.get_reciever_format() == 'form-data':
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    print("Awww yeah working smooth and clean")