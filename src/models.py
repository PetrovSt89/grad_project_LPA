from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional

from src.db import db_session

Base = declarative_base()
Base.query = db_session.query_property()


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] =mapped_column(primary_key=True)
    email: Mapped[str] =mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    is_active: Mapped[Optional[bool]]
    is_superuser: Mapped[Optional[bool]]
    is_verified: Mapped[Optional[bool]]

    tokens: Mapped['Token'] = relationship(back_populates='user')
    box: Mapped['Box'] = relationship(back_populates='creator')
    userboxs: Mapped['UserBox'] = relationship(back_populates='user')


class Token(Base):
    __tablename__ = 'tokens'
    id: Mapped[int] =mapped_column(primary_key=True)
    access_token: Mapped[str] =mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='tokens')


class Box(Base):
    __tablename__ = 'boxes'
    id: Mapped[int] =mapped_column(primary_key=True)
    boxname: Mapped[str] = mapped_column(nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    creator: Mapped['User'] = relationship(back_populates='box')
    userboxs: Mapped['UserBox'] = relationship(back_populates='box')


class UserBox(Base):
    __tablename__ = 'user_boxes'
    id: Mapped[int] =mapped_column(primary_key=True)
    box_id: Mapped[int] = mapped_column(ForeignKey('boxes.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    wishes: Mapped[str] = mapped_column(Text)
    
    user: Mapped['User'] = relationship(back_populates='userboxs')
    box: Mapped['Box'] = relationship(back_populates='userboxs')


class RandPresenter(Base):
    __tablename__ = 'rand_presenters'
    id: Mapped[int] =mapped_column(primary_key=True)
    box_id: Mapped[int] = mapped_column(ForeignKey('boxes.id'))
    presenter: Mapped[str]
    recipient: Mapped[str]

