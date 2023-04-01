# ZenGPT API Server

## Getting Started

Set up environment variables:

```shell
OPEN_AI_KEY=
DEFAULT_TOKEN_QUOTA=500000
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
PRE_SHARED_KEY=
```

The server is using DynamoDB as the database, so you need to set up the AWS credentials.
Also you need to set up the OpenAI API key and the pre-shared key for the API.

Both BFF and API server are using the same pre-shared key. Any request without the pre-shared key will be rejected as 403.

Create a virtual environment and install the dependencies:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start Server:

```shell
python src/app.py
```

## Deployment

### Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/r_fXDC?referralCode=2NjR8d)

### AWS Lightsail

server deployed on AWS LightSail us-east-1

domain: no domain yet, this service runs on port 5001 and is not exposed to the internet.

IP address:

```text
3.215.107.112
2600:1f18:115a:4d00:44bb:def9:38a7:306b
```

```text
API reverse proxy: Caddy [not used]
Language: Python 3.8
SSL: Caddy Let's encrypt
API Service: Gunicorn (with gevent)
API Framework: Flask
Service manager: Supervisor
```

This service is a stateless service, not necessary for auto snapshot and backup on server.

## API

### `GET /v1/health`

```shell
curl -X GET http://localhost:5001/v1/health
```

Response:

```json
{
  "status": "ok"
}
```

### `POST /v1/ask`

```shell
curl --request POST \
  --url http://localhost:5001/v1/ask \
  --header 'Content-Type: application/json' \
  --data '{
  "question": "Who are you?",
  "user_id": 1,
  "client_id": 1,
  "stream": false,
  "pre_shared_key": "your_pre_shared_key"
}'
```

The request body is a JSON object with the following fields:

- `question`: the question to ask the model
- `history` (optional): a list of objects to including the history of the conversation
- `client_id`: the client id of the user
- `user_id`: the user id of the user
- `stream`: whether to stream the response or not
- `pre_shared_key`: the pre-shared key for the API

Body example:

```json
{
  "question": "Who are you?",
  "user_id": 1,
  "client_id": 1,
  "stream": false,
  "history": [
    {
      "role": "user",
      "content": "hello."
    },
    {
      "role": "assistant",
      "content": "Hi."
    }
  ],
  "pre_shared_key": "your_pre_shared_key"
}
```

Response example:

```json
{
  "id": "chatcmpl-709BzPEcjA6tscXpFKX6m8E3WKCxa",
  "object": "chat.completion",
  "created": 1680269691,
  "model": "gpt-3.5-turbo-0301",
  "usage": {
    "prompt_tokens": 118,
    "completion_tokens": 57,
    "total_tokens": 175
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I am GPTDock, an AI assistant powered by the language model gpt-3.5-turbo. I am designed to assist you in a wide range of tasks, from answering questions to generating creative ideas and assisting with problem-solving. How may I assist you today?"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

#### Response as Stream

```shell
curl --request POST \
  --url http://localhost:5001/v1/ask \
  --header 'Content-Type: application/json' \
  --data '{
  "question": "Who are you?",
  "user_id": 1,
  "client_id": 1,
  "stream": true,
  "pre_shared_key": "your_pre_shared_key"
}'
```

Response example:

```text
data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"role": "assistant"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "Hello"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "!"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " I"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " am"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " G"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "PT"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "Dock"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": ","}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " an"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " AI"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " assistant"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " based"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " on"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " the"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " language"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " model"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " g"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "pt"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "-"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "3"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "."}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "5"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "-t"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "ur"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "bo"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "."}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " I"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " am"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " here"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " to"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " help"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " you"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " with"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " any"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " questions"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " or"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " tasks"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " you"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " may"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " have"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "."}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " Just"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " let"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " me"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " know"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " how"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " I"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " can"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " assist"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " you"}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "."}, "index": 0, "finish_reason": null}]}

data: {"id": "chatcmpl-709fWs9gLwfczWRasDCadymJm3vEG", "object": "chat.completion.chunk", "created": 1680271522, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]}
```

Note: The stream respond will be multiple SSE events, each event is an utf8 string starting with `data: `. and ending
with `\n\n`. The data is a JSON object with the following fields:

```json
{
  "choices": [
    {
      "delta": {
        "content": "c"
      },
      "finish_reason": null,
      "index": 0
    }
  ]
}
```



