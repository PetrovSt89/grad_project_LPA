from dataclasses import dataclass
from src.auth.models import User


class UserException(Exception):
    pass

class EmailException(Exception):
    pass

class PassException(Exception):
    pass


@dataclass
class LoginForm:
    username: str
    password: str


@dataclass
class RegistrationForm:
    username: str
    email:str
    password: str
    password2: str



    def validate_username(self):
        user_count = User.query.filter(User.username == self.username).count()
        if user_count > 0:
            raise UserException('Пользователь с таким именем уже существует')
        
    def validate_email(self):
        user_count = User.query.filter(User.email == self.email).count()
        if user_count > 0:
            raise EmailException('Пользователь с такой почтой уже существует')
        
    def pas_not_mistake(self):
        if self.password != self.password2:
            raise PassException('введены разные пароли')
