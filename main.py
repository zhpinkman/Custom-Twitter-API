from customtwitterapi import *
import os
import json
from tqdm.auto import tqdm

bearer_token = 'AAAAAAAAAAAAAAAAAAAAABb5UwEAAAAAIpS1EE%2Bu55xCxSNfnZIIM%2Fc0XJM%3DvkQGwqDgyKnPRFPYe8pdYzNRuYddk796wkZELWHdx9yIoyEXKY'
print(bearer_token)


pro_russian_accounts = [
    'CRSTAL_52',
    'thrussophile2',
    'TamrikoT',
    'AlvadisTveburg',
    'Navsteva',
    'LubimayaRussiya',
    'peterpobjecky',
    'iba1721',
    'DyallManish',
    'kagthisnov20',
    'CatEmporor',
    'vigour666',
]


for user_name in tqdm(pro_russian_accounts):
    try:
        get_user_timeline(
            bearer_token=bearer_token,
            screen_name=user_name
        )
    except Exception as e:
        print(e)
        continue
