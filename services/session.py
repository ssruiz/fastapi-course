from starlette.requests import Request

import db as _database


def get_db():
    db = _database.LocalSession()
    try:
        yield db
    finally:
        db.close()


def get_request_user(request: Request):
    user = request.state.user
    return user
