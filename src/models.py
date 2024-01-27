from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.db import db_session

Base = declarative_base()
Base.query = db_session.query_property()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id))
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    is_verified = Column(Boolean)

    tokens = relationship('Token', back_populates='user')
    box = relationship('Box', back_populates='creator')
    userboxs = relationship('UserBox', back_populates='user')


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship('User', back_populates='tokens')


class Box(Base):
    __tablename__ = 'boxes'
    id = Column(Integer, primary_key=True)
    boxname = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey(User.id))

    creator = relationship('User', back_populates='box')
    userboxs = relationship('UserBox', back_populates='box')


class UserBox(Base):
    __tablename__ = 'user_boxes'
    id = Column(Integer, primary_key=True)
    box_id = Column(Integer, ForeignKey(Box.id))
    user_id = Column(Integer, ForeignKey(User.id))
    wishes = Column(Text)

    user = relationship('User', back_populates='userboxs')
    box = relationship('Box', back_populates='userboxs')