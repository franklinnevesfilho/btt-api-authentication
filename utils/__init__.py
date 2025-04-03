from . import jwt_util
from . import password_util

def reduce_list(lst: list):
    if len(lst) == 1:
        return lst[0]
    return lst

__all__ = [
    password_util,
    jwt_util,
    reduce_list
]