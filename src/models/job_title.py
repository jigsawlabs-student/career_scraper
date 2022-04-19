from datetime import datetime
from src import db
from src.models import Position, PositionSkill, Skill
from sqlalchemy import func
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

class JobTitle(db.Model):
    __tablename__ = 'job_titles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    positions = relationship("Position", back_populates="job_title")

    @classmethod
    def top_skills(self, job_title = 'data engineer', limit = 50):
        query = db.session.query(PositionSkill.skill_id, func.count(PositionSkill.skill_id).label('total')).join(Position).join(JobTitle).filter(JobTitle.name == job_title).group_by(PositionSkill.skill_id).order_by(text('total DESC')).limit(limit)
        skill_counts =  query.all()
        skill_counts_with_names = []
        for skill_count in skill_counts:
            id = skill_count[0]
            skill_name = self.map_to_skill_names(id)
            combined = [skill_name] + list(skill_count)
            skill_counts_with_names.append(combined)
        return skill_counts_with_names

    @classmethod
    def map_to_skill_names(self, id):
        skill_name = Skill.query.get(id).name
        return skill_name

    @property
    def skills(self):
        query = PositionSkill.query.join(Position).join(JobTitle).filter(JobTitle.id == self.id)
        return query.all()

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


    