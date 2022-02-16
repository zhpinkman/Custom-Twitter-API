import os
import requests
import json


def get_user_details(bearer_token: str, user_id: str = None, screen_name: str = None):
    """
    Get the user profile given screen_name or user_id
    """
    if user_id == None and screen_name == None:
        print('Please enter either user_id or the screen_name associated with the user!')
        return 1

    if not os.path.exists('outputs/users/'):
        os.makedirs('outputs/users/')

    url = "https://api.twitter.com/1.1/users/show.json"
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}

    resp = requests.get(
        url,
        headers=headers,
        params={
            'user_id' if user_id != None else 'screen_name': user_id if user_id != None else screen_name,
        }
    )

    if resp.status_code != 200:
        print(resp.content)
        print('something went wrong!')
        return resp.status_code

    resp = resp.json()
    user_id = resp['id']
    with open(f'outputs/users/user_{user_id}', 'w') as f:
        json.dump(resp, f)
        f.close()
