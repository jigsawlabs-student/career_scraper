from bs4 import BeautifulSoup as bs
from src.adapters.page_runner import *
import src.models as models
from src import create_app, db
from tests.data.index import page


import pytest

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

@pytest.fixture(scope="module")
def cards():
    dev_url = "postgresql://postgres:postgres@localhost/test_career_scraper"
    app = create_app(dev_url)
    with app.app_context():
        engine = db.engine
        db.drop_all()
        db.create_all()

        page_runner = PageRunner(page_html = page)
        cards = page_runner.build_cards_from_html()
        yield cards

        db.drop_all()
        db.create_all()
        


def test_build_cards_from_html_fn(cards):
    assert len(cards) == 15

def test_each_card_has_title_and_id(cards):
    first_card = cards[0]
    last_card = cards[-1]
    first_card.title.lower() == 'data engineer'
    first_card.city == 'New York'
    first_card.state == 'NY'

def test_each_card_has_an_associated_page(cards):
    first_card = cards[0]
    assert type(first_card.scraped_page) == ScrapedPage

def test_scraped_page_has_fifteen_cards(cards):
    scraped_page = cards[0].scraped_page
    assert len(scraped_page.cards) == 15

def test_build_positions_from(cards):
    page_runner = PageRunner(page_html = page)
    positions = page_runner.build_positions_from(cards)
    first_position = positions[0]
    first_card = first_position.card
    assert first_position.company.name == first_card.get_company_name()
    

def test_does_not_build_an_extra_position_location(cards):
    page_runner = PageRunner(page_html = page)
    positions = page_runner.build_positions_from(cards)
    first_position = positions[0]
    assert len(first_position.position_locations) == 1

def test_saves_card_to_database(cards):
    page_runner = PageRunner(page_html = page)
    position_cards = page_runner.run()
    cards = position_cards['cards']
    positions = position_cards['positions']
    assert type(cards[0].id) == int
    assert type(positions[0].id) == int

# add about years experience

# soon will need to add skills

    

    
    
    
    









