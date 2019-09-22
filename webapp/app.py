from flask import Flask

app = Flask(__name__)

@app.route('/dev')
def index():
    return 'Hello world'


@app.route('/hello')
def hello():
    return 'Lorem Ipsum'
