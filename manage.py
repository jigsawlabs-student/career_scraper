import os
from flask.cli import FlaskGroup
import click
from src import create_app, db

dev_url = "postgresql://postgres:postgres@localhost/career_scraper"
app = create_app(dev_url)

cli = FlaskGroup(app)

from src.models import *

