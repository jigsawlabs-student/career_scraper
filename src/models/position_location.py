from datetime import datetime
from sqlalchemy.orm import relationship

from src import db
from src.models import city
class PositionLocation(db.Model):
    __tablename__ = 'position_locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    is_remote = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    position = relationship("Position", back_populates="position_locations")
    city = relationship("City", back_populates="position_locations")
    state = relationship("State", back_populates="position_locations")

