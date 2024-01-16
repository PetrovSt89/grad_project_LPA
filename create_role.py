from src.auth.models import Role
from src.db import db_session


def add_role(session, name: str):
    new_role = Role(name=name)
    session.add(new_role)
    session.commit()
    return new_role


if __name__ == "__main__":
    add_role(db_session, 'admin')