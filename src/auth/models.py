from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import relationship
from src.db import Base

metadata = MetaData()


roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)
    
user = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('role_id', Integer, ForeignKey(roles.c.id)),
    Column('is_active', Boolean, default=True),
    Column('is_superuser', Boolean, default=False),
    Column('is_verified', Boolean, default=False),
)


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

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship('User', back_populates='tokens')
