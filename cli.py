import click

import pdb

from sqlalchemy import inspect
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PASSWORD
from src.adapters.indeed_client import *
from src.adapters.position_builder import *
from src.adapters.position_skill_builder import *
from src.adapters.page_runner import *
from src.models import *
from src import db, create_app
from src.adapters.scraping_runner import ScrapingRunner
from src.adapters.seed_builder import build_skills, build_job_titles


from sqlalchemy.ext.declarative import declarative_base

import src.adapters.seed_builder as builder
Base = declarative_base()

def clear_data():
    meta = db.metadata
    engine = db.engine
    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())


db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/careers"
app = create_app(db_url)
app.app_context().push()

@click.group()
def scraper():
    pass

# Command Group
@click.group(name='tools')
def cli_tools():
    """Tool related commands"""
    pass

@cli_tools.command(name='seed_skills', help='help scrape_jobs')
def seed_skills():
    build_skills(db)

@cli_tools.command(name='seed_job_titles', help='help job_titles')
def seed_job_titles():
    build_job_titles()

# fix run scraping to maybe not take in queries for experience level
# Allow for looping through positions
@click.option('--job_title', default='data engineer')
@click.option('--location', default='United States')
@click.option('--experience', default='')
@cli_tools.command(name='build_positions', help='help build_positions')
def run_scraping(job_title, location, experience):
    ScrapingRunner().run_scraping(job_title, location, experience)

@cli_tools.command(name='build_position_skills', help='help scrape_jobs')
def build_position_skills():
    skill_builder = PositionSkillBuilder()
    skill_builder.build_skills_for_untagged_positions(db.session)




if __name__ == '__main__':
    cli_tools()