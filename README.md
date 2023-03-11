# api-server

server deployed on AWS LightSail us-east-1

domain: tbd

ip address:

      3.215.107.112
      2600:1f18:115a:4d00:3313:1a93:509:70e8
---

    API reverse proxy: Caddy
    Language: Python
    SSL: Caddy Let's encrypt
    API Service: Gunicorn
    Service manager: Supervisor

---
This service is a stateless service, not necessary for auto snapshot and backup on server.
