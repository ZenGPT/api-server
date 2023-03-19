import json
from typing import Generator

from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def response_normal(s):
    if isinstance(s, Generator):
        return Response(status=200, response=s,
                        content_type='text/data-stream',
                        headers={'Access-Control-Allow-Origin': '*'})
    if isinstance(s, str):
        return Response(status=200, response=s, content_type='application/json')
    if isinstance(s, dict):
        return Response(status=200, response=json.dumps(s), content_type='application/json')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/v1/health', methods=['GET'])
def get_health():
    return response_normal({"status": "ok"})


@app.route('/v1/ask', methods=['POST'])
def ask_question():
    obj = request.get_json()
    question = obj['question']
    user_id = obj['user_id']
    client_id = obj['client_id']
    stream = obj['stream']

    return response_normal(f"Hello World!, question: {question}, user_id: {user_id}, client_id: {client_id}, stream: {stream}")


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
