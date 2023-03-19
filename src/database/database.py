import logging
from pynamodb.exceptions import DoesNotExist, PutError
import backoff
from database_models import *

logging.getLogger('backoff').addHandler(logging.StreamHandler())

default_token_quota = 500, 000


def _init_client(client_id) -> GPTDockClientData:
    obj = GPTDockClientData(client_id=client_id, token_quota=default_token_quota)
    obj.save()
    return obj


def _init_user(user_id, client_id) -> GPTDockUserData:
    obj = GPTDockUserData(user_id=user_id, client_id=client_id)
    obj.save()
    return obj


def get_client(client_id) -> GPTDockClientData or None:
    try:
        return GPTDockClientData.get(str(client_id))
    except DoesNotExist:
        return _init_client(client_id)


def get_user(user_id, client_id) -> GPTDockUserData or None:
    try:
        return GPTDockUserData.get(str(user_id), str(client_id))
    except DoesNotExist:
        return _init_user(user_id, client_id)


@backoff.on_exception(backoff.expo, PutError, max_tries=3)
def set_client_config(client_id: str, config: dict):
    resp = get_client(client_id)
    resp.config = config
    resp.save()


@backoff.on_exception(backoff.expo, PutError, max_tries=3)
def set_user_config(user_id: str, client_id: str, config: dict):
    user = get_user(user_id, client_id)
    user.config = config
    user.save()
    return user


@backoff.on_exception(backoff.expo, PutError, max_tries=10)
def deduct_client_token(client_id, amount):
    client = get_client(client_id)
    client.token_quota -= amount
    client.save()


@backoff.on_exception(backoff.expo, PutError, max_tries=10)
def increase_user_token_used(user_id, amount):
    user = get_user(user_id)
    user.token_used += amount
    user.save()


@backoff.on_exception(backoff.expo, PutError, max_tries=10)
def reset_user_token(user_id):
    user = get_user(user_id)
    user.token_used = 0
    user.save()


@backoff.on_exception(backoff.expo, PutError, max_tries=10)
def reset_client_token(client_id):
    client = get_client(client_id)
    client.token_quota = default_token_quota
    client.save()


if __name__ == '__main__':
    pass
