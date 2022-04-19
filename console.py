from sqlalchemy import inspect

from src.adapters.indeed_client import *
from src.adapters.position_builder import *
from src.adapters.position_skill_builder import *
from src.adapters.page_runner import *
from src.models import *
from src import db, create_app
from sqlalchemy import func
from sqlalchemy.sql import text
from src.adapters.scraping_runner import ScrapingRunner
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PASSWORD

from sqlalchemy.ext.declarative import declarative_base

from src.adapters.seed_builder import *

Base = declarative_base()

def clear_data():
    meta = db.metadata
    engine = db.engine
    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())

db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/careers"
app = create_app(db_url)
app.app_context().push()



def build_skills_for_remaining_positions():
    PositionSkillBuilder.build_skills_for_untagged_positions(db.session)

