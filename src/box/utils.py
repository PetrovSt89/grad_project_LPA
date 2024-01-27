import json
import random

from typing import List, Dict

from src.models import User

def test_random(users: List[User]) -> Dict[str, str]:
    if len(users) < 2:
        return {
            users[0].username: users[0].username
        }
    if len(users) < 3:
        return {
            users[0].username: users[1].username,
            users[1].username: users[0].username
        }
    user_pres = users[:]
    user_res = users[:]
    result_dict = {}
    while user_pres and user_res:

        presenter = random.choice(user_pres)
        recipient = random.choice(user_res)
        if result_dict.get(recipient.username) == presenter.username:
            continue
        
        if recipient == presenter:
            continue

        if len(user_pres) == 1 and len(user_res) == 1 and user_res == user_pres:
            val = result_dict.popitem()
            result_dict[val[0]] = user_pres[0]
            result_dict[user_res[0]] = val[1]     

        result_dict[presenter.username] = recipient.username
        user_pres.remove(presenter)
        user_res.remove(recipient)
    return result_dict


def create_json_dependence(filename: str, person_dict: dict[str, str]) -> None:
    with open(f'{filename}.json', 'w') as json_file:
        json.dump(person_dict, json_file)


def read_json_dependence(filename: str) -> Dict[str, str]:
    with open(f'{filename}.json', 'r') as f:
        data = json.load(f)
        return data