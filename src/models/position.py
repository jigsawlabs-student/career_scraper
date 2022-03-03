from datetime import datetime
from src import db

from sqlalchemy.orm import relationship

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.String)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    minimum_salary = db.Column(db.Integer)
    maximum_salary = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="positions")

    position_locations = relationship("PositionLocation", back_populates="position")
