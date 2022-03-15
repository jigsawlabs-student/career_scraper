from bs4 import BeautifulSoup as bs
from src.models.scraped_page import *
import src.models as models
from tests.data.index import page

import pytest

@pytest.fixture
def scraped_page():
    scraped_page = ScrapedPage()
    scraped_page.set_html(page)
    yield scraped_page

def test_current_page(scraped_page):
    current_page = scraped_page.set_current_page()
    assert current_page == 2

