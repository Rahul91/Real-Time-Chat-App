from flask import Flask
import json

__author__ = 'rahul'

app = Flask('Healthify')


@app.route('/', methods=['GET'])
def hello_world():
    return json.dumps(dict(message='Hello World!!'))

if __name__ == "__main__":
    app.run(debug=True, port=3434)