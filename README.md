# api-server

server deployed on AWS LightSail us-east-1

domain: tbd

IP address:

      3.215.107.112
      2600:1f18:115a:4d00:3313:1a93:509:70e8
---

    API reverse proxy: Caddy [not used]
    Language: Python 3.8
    SSL: Caddy Let's encrypt
    API Service: Gunicorn
    API Framework: Flask
    Service manager: Supervisor

---
This service is a stateless service, not necessary for auto snapshot and backup on server.


## API

### GET /api/v1/health

    curl -X GET http://localhost:5001/api/v1/health

    {
        "status": "ok"
    }

### POST /api/v1/ask

    curl -X POST http://localhost:5001/api/v1/ask -d '{"question": "What is the weather like today?", "client_id": "1234", "user_id": "1234"}'

    [tbd openai non-stream responses]

### POST /api/v1/ask (respond as stream)

    curl -X POST http://localhost:5001/api/v1/ask -d '{"question": "What is the weather like today?", "client_id": "1234", "user_id": "1234"}' -H "Accept: text/event-stream"

    [tbd openai stream responses]
