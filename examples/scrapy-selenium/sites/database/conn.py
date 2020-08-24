# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from ..frontera.settings import SQLALCHEMYBACKEND_ENGINE


def create_mysql_engine():
    engine = create_engine(
        SQLALCHEMYBACKEND_ENGINE,
    )
    return engine
