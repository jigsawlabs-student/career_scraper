import os
from flask.cli import FlaskGroup
import click
from src import app, db

cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
