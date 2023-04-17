from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler
from utils import *
from database import database
from open_ai import function_call
from monitor import axiom_client
load_dotenv()

app = Flask(__name__)
CORS(app)

scheduler = APScheduler()
moniter_enable=os.getenv('MONITER_ENABLE','False')=='True'
if moniter_enable:
    scheduler.init_app(app)
    scheduler.start()

@scheduler.task('interval', id='heartbeat', seconds=int(os.getenv('MONITER_HEARBEAT_INTERVAL_SECONDS',60)),misfire_grace_time=int(os.getenv('MONITER_DEFAULT_MISFIRE_GRACE_TIME_SECONDS',60)))
def heartbeat_task():
    axiom_client.ingest_heartbeat()

@scheduler.task('interval', id='users_count', seconds=int(os.getenv('MONITER_USERS_COUNT_INTERVAL_SECONDS',60)),misfire_grace_time=int(os.getenv('MONITER_DEFAULT_MISFIRE_GRACE_TIME_SECONDS',60)))
def users_count_task():
    axiom_client.ingest_users_count(database.get_users_count())

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/v1/health', methods=['GET'])
def get_health():
    return response_normal({"status": "ok"})


@app.route('/v1/client/info', methods=['GET'])
@monitor_decorator()
@auth_decorator()
def get_client_info():
    client_id = request.args.get('client_id')
    product_id = request.args.get('product_id')
    if not client_id:
        return response_bad_request('client_id must be provided')

    client = database.get_client(client_id, product_id)
    if not client:
        return response_not_found('client not found')

    return response_normal({'client_id': client.client_id, 'quota_used': client.max_quota - client.token_quota, 'max_quota': client.max_quota})


@app.route('/v1/ask', methods=['POST'])
@monitor_decorator()
@auth_decorator()
def ask_question():
    obj = request.get_json()
    try:
        user_id = str(obj['user_id'])
        client_id = str(obj['client_id'])
        product_id = str(obj['product_id'])
        stream = obj['stream']
        question = obj['question']
    except KeyError:
        return response_bad_request('Missing required parameters, user_id, client_id, stream, question, product_id must be provided')
    history = obj.get('history') or []
    history.append({"role": "user", "content": question})
    client = database.get_client(client_id, product_id)
    prompt, tokens = function_call.get_prompt(history)

    # now we check if the client has enough tokens (roughly 2x of prompt tokens)
    if tokens * 2 > client.token_quota:
        return response_not_enough_token

    request_data = function_call.get_request_data(prompt, tokens, f'{client_id}_{user_id}', stream)
    res = function_call.open_ai_call(request_data)
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
                            'delta': {}
                        }
                    ]
                }
                yield 'data: ' + json.dumps(response) + '\n\n'
            yield 'data: [DONE]\n\n'
            completion_tokens_stream = function_call.get_token_count(completion_content)
            credit_stream = prompt_tokens_stream + completion_tokens_stream
            database.deduct_client_token(client_id, product_id, credit_stream)
            database.increase_user_token_used(user_id, client_id, product_id, credit_stream)
        return response_normal(get_res())
    else:
        completion_tokens = res['usage']['completion_tokens']
        prompt_tokens = res['usage']['prompt_tokens']
        total_tokens = completion_tokens + prompt_tokens + tokens
        database.deduct_client_token(client_id, product_id, total_tokens)
        database.increase_user_token_used(user_id, client_id, product_id, total_tokens)
        return response_normal(res)


if __name__ == '__main__':
    app.run('0.0.0.0', 5001)
