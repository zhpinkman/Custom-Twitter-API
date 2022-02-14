import requests
import json
import os


def get_user_timeline(bearer_token: str, user_id: str = None, username: str = None, replace: bool = False):
    """
        Get the whole timeline of the user limited by Twitter API to up to 3200 tweets including the retweets
    """
    if user_id == None and username == None:
        print('Please enter either user_id or the username associated with the user!')
        return 1
    if not os.path.exists('outputs/'):
        os.mkdir('outputs')
    endpoint = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}

    users_tweets = []
    print('getting the conversations of user {}'.format(
        user_id if user_id != None else username))
    max_id = None
    while True:
        if max_id == None:
            resp = requests.get(
                endpoint,
                params={
                    'count': 200,
                    'user_id' if user_id != None else 'screen_name': user_id if user_id != None else username,
                },
                headers=headers
            )
        else:
            resp = requests.get(
                endpoint,
                params={
                    'count': 200,
                    'user_id' if user_id != None else 'screen_name': user_id if user_id != None else username,
                    'max_id': max_id
                },
                headers=headers
            )
        if resp.status_code != 200:
            print(resp.content)
            print('Something went wrong!')
            return resp.status_code
        resp = resp.json()
        if len(resp) == 0:
            return 1
        if len(resp) == 1:
            break

        if len(users_tweets) and resp[0]['id'] == users_tweets[-1]['id']:
            users_tweets.extend(resp[1:])
        else:
            users_tweets.extend(resp)

        if not replace:

            if os.path.exists(f"outputs/user_{users_tweets[0]['user']['id']}.json"):
                return 0

        max_id = resp[-1]['id']
    user_id = users_tweets[0]['user']['id']
    print(f'num of tweets for user_id {user_id} : {len(users_tweets)}')
    with open(f'outputs/user_{user_id}.json', 'w') as f:
        json.dump(users_tweets, f)
        f.close()
