from src import db
from bs4 import BeautifulSoup as bs
from datetime import datetime
from sqlalchemy.orm import relationship
import re

class ScrapedPage(db.Model):
    __tablename__ = 'scraped_pages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    html = db.Column(db.Text)
    page_number = db.Column(db.Integer)
    scraping_id = db.Column(db.Integer, db.ForeignKey('scrapings.id'))
    scraping = relationship("Scraping", back_populates="scraped_pages")
    cards = relationship("Card", back_populates="scraped_page")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def set_html(self, html):
        self.html = str(html)
        self.bs = bs(html)

    def run(self):
        self.set_current_page()

    def set_current_page(self):
        text = self.bs.find('div', {'id': 'searchCountPages'}).text
        page_num = re.findall(r'\d+', text)[0]
        self.page_number = int(page_num)
        return self.page_number

    
        



