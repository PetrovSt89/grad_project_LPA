import json
import random

from typing import List

from src.models import User

def test_random(users: List[User]) -> dict[str, str]:
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
        result_dict[presenter.username] = recipient.username
        user_pres.remove(presenter)
        user_res.remove(recipient)
    return result_dict


def create_json_dependence(filename: str, person_dict: dict[str, str]):
    with open(f'{filename}.json', 'w') as json_file:
        json.dump(person_dict, json_file)


def read_json_dependence(filename: str):
    with open(f'{filename}.json', 'r') as f:
        data = json.load(f)
        return data