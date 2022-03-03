from datetime import datetime
from src import db
import src.models as models
from sqlalchemy.orm import relationship

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    state = relationship("State", back_populates="cities")
    position_locations = relationship("PositionLocation", back_populates="city")

    @property
    def positions(self):
        query = models.Position.query.join(models.PositionLocation).join(City).filter(City.id == self.id)
        return query.all()