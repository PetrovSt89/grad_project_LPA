import json
import random
from src.models import Role
from src.db import db_session
from sqlalchemy import select


def add_role(session, name: str):
    new_role = Role(name=name)
    session.add(new_role)
    session.commit()
    return new_role



def update_role(session, name:str, new_name: str):
    role = db_session.scalar(select(Role).where(Role.name == name))
    role.name = new_name
    session.commit()


def delete_role(session, name: str):
    role = db_session.scalar(select(Role).where(Role.name == name))
    db_session.delete(role)
    db_session.commit()



def test_random(users):
    user_pres = users[:]
    user_res = users[:]
    result_list = {}
    while user_pres and user_res:

        presenter = random.choice(user_pres)
        recipient = random.choice(user_res)
        if result_list.get(recipient) == presenter:
            continue
        if recipient == presenter:
            continue
        result_list[presenter] = recipient
        user_pres.remove(presenter)
        user_res.remove(recipient)
    return result_list


def create_json_dependence(person_dict: dict[str, str]):
    with open('person.json', 'w') as json_file:
        json.dump(person_dict, json_file)


def read_json_dependence(file: str):
    with open(file, 'r') as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    # update_role(session=db_session, name='ad', new_name='soplyak')
    # add_role(db_session, 'ad')
    # delete_role(db_session, 'soplyak')
    # users = ['Stas', 'Dasha', 'Mama', 'Sasha']
    # print(test_random(users))
    # person_dict = {'Stas': 'Petrov',
    #                'Dasha': 'Minina'}
    # print(create_json_dependence(person_dict=person_dict))
    data = read_json_dependence(file='person.json')
    print(data)