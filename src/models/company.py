from datetime import datetime
from src import db

from sqlalchemy.orm import relationship

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    positions = relationship("Position", back_populates="company")