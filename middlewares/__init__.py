import sqlalchemy.orm as orm
from aiogram import Dispatcher

from .user_mw import UserMiddleware
from .exeption_mw import ForbiddenErrorMiddleware


def setup(dp: Dispatcher, sessionmaker: orm.sessionmaker):
    dp.update.outer_middleware(ForbiddenErrorMiddleware())
    dp.update.outer_middleware(UserMiddleware(sessionmaker))
