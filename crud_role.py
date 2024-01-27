from enum import Enum
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


if __name__ == "__main__":
    # update_role(session=db_session, name='ad', new_name='soplyak')
    # add_role(db_session, 'ad')
    # delete_role(db_session, 'soplyak')
    print('hello')
