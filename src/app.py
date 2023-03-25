from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from utils import *
from database import database
from open_ai import function_call

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/v1/health', methods=['GET'])
def get_health():
    return response_normal({"status": "ok"})


@app.route('/v1/ask', methods=['POST'])
def ask_question():
    obj = request.get_json()
    try:
        user_id = obj['user_id']
        client_id = obj['client_id']
        stream = obj['stream']
        question = obj['question']
    except KeyError:
        return response_bad_request('Missing required parameters, user_id, client_id, stream, question must be provided')

    history = obj.get('history') or []
    history.append({"role": "user", "content": question})
    client = database.get_client(client_id)
    prompt, tokens = function_call.get_prompt(history)

    # now we check if the client has enough tokens (roughly 2x of prompt tokens)
    if tokens * 2 > client.token_quota:
        return response_not_enough_token

    request_data = function_call.get_request_data(prompt, f'{client_id}_{user_id}', stream)

    if stream:
        def get_res():
            prompt_tokens_stream = tokens
            completion_content = ''
            try:
                for response in res:
                    completion_content += response['choices'][0]['delta'].get('content') or ''
                    yield 'data: ' + json.dumps(response) + '\n\n'
            except Exception:
                # here we catch all exceptions as a stop of generating the response
                response = {
                    'choices': [
                        {
                            'finish_reason': 'stop',
                            'text': ''
                        }
                    ]
                }
                yield 'data: ' + json.dumps(response) + '\n\n'

            completion_tokens_stream = function_call.get_token_count(completion_content)
            credit_stream = prompt_tokens_stream + completion_tokens_stream
            database.deduct_client_token(client_id, credit_stream)
            database.increase_user_token_used(user_id, client_id, credit_stream)
        return response_normal(get_res())

    else:
        res = function_call.open_ai_call(request_data)
        completion_tokens = res['usage']['completion_tokens']
        prompt_tokens = res['usage']['prompt_tokens']
        total_tokens = completion_tokens + prompt_tokens + tokens
        database.deduct_client_token(client_id, total_tokens)
        database.increase_user_token_used(user_id, client_id, total_tokens)
        return response_normal(res)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
