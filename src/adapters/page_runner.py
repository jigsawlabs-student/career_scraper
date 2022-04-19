from src.models import *
import re
from src.adapters.indeed_client import get_page
from src.adapters.position_builder import PositionBuilder
from src import db
class PageRunner():
    def __init__(self, page_html = '', scraped_page = ''):
        if page_html:
            self.page_html = page_html
            self.scraped_page = ScrapedPage()
            self.scraped_page.set_html(page_html)
        else:
            self.scraped_page = scraped_page
            self.page_html = scraped_page.html

    def run(self, query = ''):
        self.scraped_page.run()
        cards = self.build_cards_from_html()
        positions = self.build_positions_from(cards, query)
        db.session.commit()
        return {'scraped_page': self.scraped_page, 'positions': positions, 'cards': cards}

    def build_cards_from_html(self):
        html_cards = self.get_html_cards_from(self.scraped_page)
        
        for html_card in html_cards:    
            card = Card.build_card_from(html_card)
            db.session.add(card)
            self.scraped_page.cards.append(card)
        return self.scraped_page.cards

    def build_positions_from(self, cards, query = ''):
        positions = []
        for card in cards:
            position = self.build_position_from(card, query)
            positions.append(position)
        
        return positions

    def build_position_from(self, card, query):
        builder = PositionBuilder(card)
        position = builder.run()
        position.query_string = query
        job_title = JobTitle.query.filter(JobTitle.name == query).first()
        if job_title:
            position.job_title = job_title
        db.session.add(position)
        return position

    def get_html_cards_from(self, page):
        cards = page.bs.findAll('a', id=re.compile('^job_'))
        return cards

    def get_or_build(self, db, model, **kwargs):
        instance = db.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            db.session.add(instance)
            return instance

