from datetime import datetime
from src import db
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)