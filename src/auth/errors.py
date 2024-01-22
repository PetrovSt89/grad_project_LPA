from fastapi import HTTPException


class HTTPExceptionUser(HTTPException):
    pass

class HTTPExceptionToken(HTTPException):
    pass

class HTTPExceptionPass(HTTPException):
    pass

class HTTPExceptionDifPass(HTTPException):
    pass

class HTTPExceptionAuth(HTTPException):
    pass

class HTTPExceptionEmail(HTTPException):
    pass

class HTTPExceptionRepUser(HTTPException):
    pass

class HTTPExceptionRepToken(HTTPException):
    pass