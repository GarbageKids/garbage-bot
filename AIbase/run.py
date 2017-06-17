from flask import Flask
from utilities.settings import Settings
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/chatter', methods=[Settings.get_reciever_method()])
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()