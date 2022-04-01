from datetime import datetime
from src import db
import src.models as models
from sqlalchemy.orm import relationship

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)