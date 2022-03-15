from bs4 import BeautifulSoup as bs
from src.adapters.position_builder import *
from src.adapters.page_runner import *
import src.models as models
from src import create_app, db
from tests.data.index import page


import pytest

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def clear_data():
    meta = db.metadata
    engine = db.engine
    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())
    

def cleanup(app, session):
    session.close()
    engine_container = db.get_engine(app)
    engine_container.dispose()

@pytest.fixture(scope="module")
def cards():
    dev_url = "postgresql://postgres:postgres@localhost/test_career_scraper"
    app = create_app(dev_url)
    with app.app_context():
        clear_data()
        cleanup(app, db.session)
        
        page_runner = PageRunner(page_html = page)
        cards = page_runner.build_cards_from_html()
        yield cards

        clear_data()
        cleanup(app, db.session)

        

def test_each_builds_related_position(cards):
    first_card = cards[0]
    position_builder = PositionBuilder(first_card)
    position = position_builder.run()
    assert position.title == 'Training Data Management Platform - Data Engineer'
    
    assert position.minimum_salary == None
    assert position.maximum_salary == None
    assert position.company.name == 'JPMorgan Chase Bank, N.A.'

    second_card = cards[1]
    position_builder = PositionBuilder(second_card)
    second_position = position_builder.run()

    assert second_position.company.name == 'UBS'
    assert second_position.date_posted.day == (datetime.today() - timedelta(days=30)).day
    third_card = cards[2]
    position_builder = PositionBuilder(third_card)
    third_position = position_builder.run()

    assert third_position.minimum_experience == 1
    assert third_position.maximum_experience == 5
    

    
