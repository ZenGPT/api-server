# Development

## Prerequisites
1. Python 3.8 ~ 3.10. AWS sdk is not compatible with Python 3.11 yet.
2. AWS account set up with credentials in `~/.aws/config`

## Setup

    pip3 install -r requirements.txt
    cd src
    python3.x app.py

# api-server

server deployed on AWS LightSail us-east-1

domain: no domain yet, this service runs on port 5001 and is not exposed to the internet.

IP address:

      3.215.107.112
      2600:1f18:115a:4d00:44bb:def9:38a7:306b
---

    API reverse proxy: Caddy [not used]
    Language: Python 3.8
    SSL: Caddy Let's encrypt
    API Service: Gunicorn (with gevent)
    API Framework: Flask
    Service manager: Supervisor

---
This service is a stateless service, not necessary for auto snapshot and backup on server.


## API

### GET /v1/health

    curl -X GET http://localhost:5001/api/v1/health

    {
        "status": "ok"
    }

### POST /v1/ask

The request body is a JSON object with the following fields:

- `question`: the question to ask the model
- (optional) `history`: a list of objects to including the history of the conversation
    ```json
    [
        {
            "role": "user",
            "content": "hello."
        },
        {
            "role": "assistant",
            "content": "Hi."
        },
        ...
    ]   
    ```
- `client_id`: the client id of the user
- `user_id`: the user id of the user
- `stream`: whether to stream the response or not



    curl -X POST http://localhost:5001/v1/ask -d '{"question": "What is the weather like today?", "client_id": "1234", "user_id": "1234", "stream": false}' -H "Content-Type: application/json"

    {
        "id": "chatcmpl-6xqiwPWAdmSblSYSxOC5TkJHYL3qi",
        "bject": "chat.completion",
        "ocreated": 1679722042,
        "model": "gpt-3.5-turbo-0301",
        "usage": {
            "prompt_tokens": 109,
            "completion_tokens": 27,
            "total_tokens": 136
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "I don't know man."
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
    }

### POST /v1/ask (respond as stream)

The request body is a JSON object with the following fields:

- `question`: the question to ask the model
- (optional) `history`: a list of objects to including the history of the conversation
    ```json
    [
        {
            "role": "user",
            "content": "hello."
        },
        {
            "role": "assistant",
            "content": "Hi."
        },
        ...
    ]   
    ```
- `client_id`: the client id of the user
- `user_id`: the user id of the user
- `stream`: whether to stream the response or not



    curl -X POST http://localhost:5001/v1/ask -d '{"question": "What is the weather like today?", "client_id": "1234", "user_id": "1234", "stream": true}' -H "Accept: text/event-stream" -H "Content-Type: application/json"

    data: {"id": "chatcmpl-6xsye6iaNWJWwhcWMjJiGqGEX35S5", "object": "chat.completion.chunk", "created": 1679730704, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"role": "assistant"}, "index": 0, "finish_reason": null}]}
    
    data: {"id": "chatcmpl-6xsye6iaNWJWwhcWMjJiGqGEX35S5", "object": "chat.completion.chunk", "created": 1679730704, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "I"}, "index": 0, "finish_reason": null}]}

    data: {"id": "chatcmpl-6xsye6iaNWJWwhcWMjJiGqGEX35S5", "object": "chat.completion.chunk", "created": 1679730704, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " Channel"}, "index": 0, "finish_reason": null}]}

    data: {"id": "chatcmpl-6xsye6iaNWJWwhcWMjJiGqGEX35S5", "object": "chat.completion.chunk", "created": 1679730704, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": " Channel"}, "index": 0, "finish_reason": null}]}

    data: {"id": "chatcmpl-6xsye6iaNWJWwhcWMjJiGqGEX35S5", "object": "chat.completion.chunk", "created": 1679730704, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {"content": "."}, "index": 0, "finish_reason": null}]}
    
    data: {"id": "chatcmpl-6xsye6iaNWJWwhcWMjJiGqGEX35S5", "object": "chat.completion.chunk", "created": 1679730704, "model": "gpt-3.5-turbo-0301", "choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]}

> Note: The stream respond will be multiple SSE events, each event is an utf8 string starting with `data: `. and ending with `\n\n`. The data is a JSON object with the following fields:
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



