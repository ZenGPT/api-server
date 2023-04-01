import logging
import os

from pynamodb.exceptions import DoesNotExist, PutError
import backoff
from database.database_models import *
from dotenv import load_dotenv

load_dotenv()

logging.getLogger('backoff').addHandler(logging.StreamHandler())

default_token_quota = int(os.getenv('DEFAULT_TOKEN_QUOTA', '500000'))


def _init_client(client_id) -> GPTDockClientData:
    """
    Initialize a new client, with default token quota
    the quota will be used until 0, then the client will be blocked

    reset the quota every month.

    // TODO: reset quota every month

    :param client_id:
    :return:
    """
    obj = GPTDockClientData(client_id=client_id, token_quota=default_token_quota, max_quota=default_token_quota)
    obj.save()
    return obj


def _init_user(user_id, client_id) -> GPTDockUserData:
    """
    Initialize a new user, user don't have quota but keep track of how many tokens they used
    in future we will quote user based on the client settings, e.g., 10% of the client quota per user.

    :param user_id:
    :param client_id:
    :return:
    """
    obj = GPTDockUserData(user_id=user_id, client_id=client_id)
    obj.save()
    return obj


def check_client(client_id) -> GPTDockClientData or None:
    try:
        return GPTDockClientData.get(str(client_id))
    except DoesNotExist:
        return None


def get_client(client_id) -> GPTDockClientData:
    try:
        return GPTDockClientData.get(str(client_id))
    except DoesNotExist:
        return _init_client(client_id)


def get_user(user_id, client_id) -> GPTDockUserData:
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
def increase_user_token_used(user_id, client_id, amount):
    user = get_user(user_id, client_id)
    user.token_used += amount
    user.save()


@backoff.on_exception(backoff.expo, PutError, max_tries=10)
def reset_user_token(user_id, client_id):
    user = get_user(user_id, client_id)
    user.token_used = 0
    user.save()


@backoff.on_exception(backoff.expo, PutError, max_tries=10)
def reset_client_token(client_id):
    client = get_client(client_id)
    client.token_quota = default_token_quota
    client.save()


if __name__ == '__main__':
    pass
