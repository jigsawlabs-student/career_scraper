from src import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Scraping(db.Model):
    __tablename__ = 'scrapings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query_string = db.Column(db.String(128))
    location = db.Column(db.String(128))
    experience_level = db.Column(db.String(128))
    total_jobs = db.Column(db.Integer)
    scraped_pages = relationship("ScrapedPage", back_populates="scraping")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    

