from datetime import datetime
from src import db
import src.models as models
from sqlalchemy.orm import relationship

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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
    def find_by_name(self, name):
        return db.session.query(Skill).filter(Skill.name == name).all()
