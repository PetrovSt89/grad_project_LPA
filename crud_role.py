from src.models import Role
from src.db import db_session
from sqlalchemy import update, delete


def add_role(session, name: str) -> None:
    new_role = Role(name=name)
    session.add(new_role)
    session.commit()


def update_role(session, name:str, new_name: str) -> None:
    role = (update(Role).where(Role.name == name).values(name=new_name))
    session.execute(role)
    session.commit()


def delete_role(session, name: str) -> None:
    role = (delete(Role).where(Role.name == name))
    session.execute(role)
    session.commit()


if __name__ == "__main__":
    # update_role(session=db_session, name='userok', new_name='user')
    # add_role(db_session, 'admin')
    # delete_role(db_session, 'ad')
    print('hello')
