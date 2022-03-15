from src.adapters.scraping_runner import ScrapingRunner
from src import db, create_app
import pytest 



@pytest.fixture(scope="module")
def build_db():
    test_url = "postgresql://postgres:postgres@localhost/test_career_scraper"
    app = create_app(test_url)
    with app.app_context():
        engine = db.engine
        db.drop_all()
        db.create_all()
        
        yield

        db.drop_all()
        db.create_all()

def test_scraping_runner(build_db):
    runner = ScrapingRunner()
    page = runner.run_scraping(position = 'data engineer', location = 'nyc',
     experience_level = 'entry_level')
    
    assert page == page
    

