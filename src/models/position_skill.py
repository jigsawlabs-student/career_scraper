from datetime import datetime
from src import db
import src.models as models
from sqlalchemy.orm import relationship

class PositionSkill(db.Model):
    __tablename__ = 'position_skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))