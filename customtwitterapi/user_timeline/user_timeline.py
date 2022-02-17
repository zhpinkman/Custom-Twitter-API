from typing import List
import time
import requests
import json
import os
from ..consts import status_codes, CustomErrorStatusCode


def logging(user_id: str, screen_name: str):
    with open('outputs/log.txt', 'a') as f:
        if user_id:
            f.write(f'{user_id}\n')
        if screen_name:
            f.write(f'{screen_name}\n')
        f.close()


def get_logs():
    with open('outputs/log.txt', 'r') as f:
        user_id_user_names = f.read().splitlines()
        f.close()
    return user_id_user_names


def do_pre_check(user_id: str, screen_name: str):
    history_ids = get_logs()
    if user_id in history_ids or screen_name in history_ids:
        raise CustomErrorStatusCode(
            {'message': status_codes['ALREADY_CRAWLED']})
    if user_id == None and screen_name == None:
        raise CustomErrorStatusCode(
            {'message': status_codes['EMPTY_USER_ID_NAME']})
    if not os.path.exists('outputs/tweets/'):
        os.makedirs('outputs/tweets/')


def make_request(user_id: str, screen_name: str, max_id: int, bearer_token: str):
    endpoint = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
    if max_id == None:
        resp = requests.get(
            endpoint,
            params={
                'count': 200,
                'user_id' if user_id != None else 'screen_name': user_id if user_id != None else screen_name,
            },
            headers=headers
        )
    else:
        resp = requests.get(
            endpoint,
            params={
                'count': 200,
                'user_id' if user_id != None else 'screen_name': user_id if user_id != None else screen_name,
                'max_id': max_id
            },
            headers=headers
        )
    if resp.status_code != 200:
        logging(user_id, screen_name)
        if resp.status_code == 429:
            raise CustomErrorStatusCode(
                {'message': status_codes['RATE_LIMIT_REACHED']})
        raise CustomErrorStatusCode({'message': resp.content})
    return resp.json()


def is_last_message(resp: List[dict]):
    if len(resp) == 0:
        raise CustomErrorStatusCode({'message': status_codes['NO_DATA']})
    if len(resp) == 1:
        return True
    return False


def get_user_timeline(bearer_token: str, user_id: str = None, screen_name: str = None):
    """
        Get the whole timeline of the user limited by Twitter API to up to 3200 tweets including the retweets
    """
    do_pre_check(user_id, screen_name)

    users_tweets = []
    max_id = None
    while True:
        try:
            resp = make_request(user_id, screen_name, max_id, bearer_token)
        except CustomErrorStatusCode as e:
            details = e.args[0]
            if details['message'] == status_codes['RATE_LIMIT_REACHED']:
                print('Sleeping for 15 minutes')
                time.sleep(15 * 60)
                continue
            else:
                raise e
        if is_last_message(resp):
            break

        if len(users_tweets) and resp[0]['id'] == users_tweets[-1]['id']:
            users_tweets.extend(resp[1:])
        else:
            users_tweets.extend(resp)

        max_id = resp[-1]['id']

    user_id = resp[0]['user']['id']
    if max_id == None:
        users_tweets.append(resp[0])
    print(f'num of tweets for user_id {user_id} : {len(users_tweets)}')
    logging(user_id, screen_name)
    with open(f'outputs/tweets/user_{user_id}.json', 'w') as f:
        json.dump(users_tweets, f)
        f.close()
