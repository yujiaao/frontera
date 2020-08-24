# -*- coding: utf-8 -*-

# from .conn import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from ..frontera.settings import SQLALCHEMYBACKEND_ENGINE


# engine = create_mysql_engine()

# conn = engine.connect()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMYBACKEND_ENGINE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)



def reset_database():
    db.drop_all()
    db.create_all()


