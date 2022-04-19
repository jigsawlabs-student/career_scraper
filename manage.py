import os
from flask.cli import FlaskGroup
import click
from src import create_app, db
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PASSWORD

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/careers"

app = create_app(db_url)

cli = FlaskGroup(app)

from src.models import *

