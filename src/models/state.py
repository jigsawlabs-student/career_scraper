from datetime import datetime
from src import db
from sqlalchemy.orm import relationship

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    cities = relationship("City", back_populates="state")
    position_locations = relationship("PositionLocation", back_populates="state")
