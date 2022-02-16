from customtwitterapi.consts import status_codes, CustomErrorStatusCode
from customtwitterapi.user_timeline.user_timeline import get_user_timeline
from customtwitterapi.user_profile.user_profile import get_user_details
from customtwitterapi.user_relations.user_relations import get_user_relations
import os


if not os.path.exists('outputs/'):
    os.mkdir('outputs/')
if not os.path.exists('outputs/log.txt'):
    open('outputs/log.txt', 'w').close()
