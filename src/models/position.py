from datetime import datetime
from src import db
import src.models as models

from sqlalchemy.orm import relationship

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.String)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    minimum_salary = db.Column(db.Integer)
    maximum_salary = db.Column(db.Integer)
    minimum_experience = db.Column(db.Integer)
    maximum_experience = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    date_posted = db.Column(db.DateTime)
    query_string = db.Column(db.String)
    job_title_id = db.Column(db.Integer, db.ForeignKey('job_titles.id'))
    job_title = relationship("JobTitle", back_populates="positions")
    
    company = relationship("Company", back_populates="positions")
    card = relationship("Card", back_populates="position")
    
    position_locations = relationship("PositionLocation", back_populates="position")
    position_skills = relationship("PositionSkill", back_populates="position")

    # add skills query
    
    @property
    def skills(self):
        query = models.Skill.query.join(models.PositionSkill).join(Position).filter(models.PositionSkill.position_id == self.id)
        return query.all()

    