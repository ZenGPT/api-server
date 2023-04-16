import os
import requests
import axiom
from dotenv import load_dotenv

load_dotenv()

default_dataset=os.getenv('MONITER_AXIOM_DATASET')
moniter_enable=os.getenv('MONITER_ENABLE','False')=='True'
heartbeat_url=os.getenv('MONITER_HEARBEAT_URL')
def ingest_heartbeat():
    if not moniter_enable:
        return
    response=requests.get(heartbeat_url)
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
             "event_type": "heartbeat", 
             "url": heartbeat_url,
             "status_code": response.status_code
            }
        ])
    
def ingest_http_request(request,response):
    if not moniter_enable:
        return
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
              "event_type": "http_request",
              "params":request.get_json(),
              "path": request.path,
              "method":request.method,
              "status": response.status_code
            }
        ])

def ingest_token_usage(user_id, client_id, product_id, amount):
    if not moniter_enable:
        return
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
              "event_type": "token_usage",
              "user_id":user_id,
              "client_id": client_id,
              "product_id":product_id,
              "amount": amount
            }
        ])
    
def ingest_users_count(count):
    if not moniter_enable:
        return
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
              "event_type": "users_count",
              "count": count
            }
        ])
    
def create_client():
    return axiom.Client(os.getenv('MONITER_AXIOM_API_TOKEN'), os.getenv('MONITER_AXIOM_ORG_ID'))