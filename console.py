from sqlalchemy import inspect

from src.adapters.indeed_client import *
from src.adapters.position_builder import *
from src.adapters.page_runner import *
from src.models import *
from src import db, create_app
from src.adapters.scraping_runner import ScrapingRunner

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def clear_data():
    meta = db.metadata
    engine = db.engine
    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())

# cards = get_job_cards(position = 'data engineer', location = 'United States', start = 0)
# first_card = cards[0]

# state = State(name = 'New York')
# new_york.cities.append(city)
# db.session.add(new_york)
# db.session.commit()
    # both city and state now added
db_url = "postgresql://postgres:postgres@localhost/career_scraper"
app = create_app(db_url)
app.app_context().push()

runner = ScrapingRunner()
# runner.run_scraping(position = 'data engineer', location = 'nyc', experience_level = 'entry_level')
