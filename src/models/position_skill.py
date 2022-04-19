from datetime import datetime
from src import db
import src.models as models
from sqlalchemy.orm import relationship
from sqlalchemy import func

class PositionSkill(db.Model):
    __tablename__ = 'position_skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'))
    
    position = relationship("Position", back_populates="position_skills")
    skill = relationship("Skill", back_populates="position_skills")

    @classmethod
    def get_or_create(Klass, session, **kwargs):
        instance = session.query(Klass).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = Klass(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    @classmethod
    def last_position_id(self):
        return db.session.query(func.max(self.position_id)).first()[0]