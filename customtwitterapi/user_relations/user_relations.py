import os
import json
import requests
import time

from customtwitterapi.user_timeline.user_timeline import is_last_message
from ..consts import status_codes, CustomErrorStatusCode


def make_request(user_id: str, cursor: int, bearer_token: str, relation_type: str):
    endpoint = f'https://api.twitter.com/2/users/{user_id}/{relation_type}'
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
    if cursor == None:
        resp = requests.get(
            endpoint,
            params={
                'max_results': 1000,
            },
            headers=headers
        )
    else:
        resp = requests.get(
            endpoint,
            params={
                'max_results': 1000,
                'pagination_token': cursor,

            },
            headers=headers
        )
    if resp.status_code != 200:
        if resp.status_code == 429:
            raise CustomErrorStatusCode(
                {'message': status_codes['RATE_LIMIT_REACHED']})
        raise CustomErrorStatusCode({'message': resp.content})
    return resp.json()


def is_last_message(resp):
    if 'next_token' not in resp['meta'].keys():
        return True
    return False


def do_pre_check(user_id: str, relation_type: str):
    if os.path.exists(f'outputs/{relation_type}/user_{user_id}.json'):
        raise CustomErrorStatusCode({
            'message': status_codes['ALREADY_CRAWLED']
        })


def get_user_relations(bearer_token: str, user_id: str, relation_type: str):
    if not os.path.exists(f'outputs/{relation_type}'):
        os.mkdir(f'outputs/{relation_type}')

    do_pre_check(user_id, relation_type)
    users_relations = []
    cursor = None
    while True:
        try:
            resp = make_request(user_id, cursor, bearer_token, relation_type)
        except CustomErrorStatusCode as e:
            details = e.args[0]
            if details['message'] == status_codes['RATE_LIMIT_REACHED']:
                print('Sleeping for 15 minutes')
                time.sleep(15 * 60)
                continue
            else:
                raise e

        users_relations.extend(resp['data'])
        if is_last_message(resp):
            break

        cursor = resp['meta']['next_token']

    with open(f'outputs/{relation_type}/user_{user_id}.json', 'w') as f:
        json.dump(users_relations, f)
        f.close()
