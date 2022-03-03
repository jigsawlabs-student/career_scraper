from datetime import datetime
from src import db
class PositionLocation(db.Model):
    __tablename__ = 'position_locations'
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    is_remote = db.Column(db.Boolean)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)