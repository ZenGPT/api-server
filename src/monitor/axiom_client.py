import os
import requests
import axiom
import gevent
from dotenv import load_dotenv

load_dotenv()

default_dataset=os.getenv('MONITOR_AXIOM_DATASET')
monitor_enable=os.getenv('MONITOR_ENABLE','False')=='True'
heartbeat_url=os.getenv('MONITOR_HEARBEAT_URL')
def ingest_heartbeat():
    if not monitor_enable:
        return
    response=requests.get(heartbeat_url)
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
             "event_type": "heartbeat", 
             "url": heartbeat_url,
             "status_code": response.status_code,
             "worker_id": get_worker_id()
            }
        ])
    
def ingest_http_request(request,response):
    if not monitor_enable:
        return
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
              "event_type": "http_request",
              "params":request.get_json(),
              "path": request.path,
              "method":request.method,
              "status": response.status_code,
              "worker_id": get_worker_id()
            }
        ])

def ingest_token_usage(user_id, client_id, product_id, amount):
    if not monitor_enable:
        return
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
              "event_type": "token_usage",
              "user_id":user_id,
              "client_id": client_id,
              "product_id":product_id,
              "amount": amount,
              "worker_id": get_worker_id()
            }
        ])
    
def ingest_users_count(count):
    if not monitor_enable:
        return
    create_client().ingest_events(
        dataset=default_dataset,
        events=[
            {
              "event_type": "users_count",
              "count": count,
              "worker_id": get_worker_id()
            }
        ])
    
def create_client():
    return axiom.Client(os.getenv('MONITOR_AXIOM_API_TOKEN'), os.getenv('MONITOR_AXIOM_ORG_ID'))

def get_worker_id():
    return os.getpid()