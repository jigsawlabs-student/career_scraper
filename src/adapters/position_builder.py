from src.adapters.indeed_client import *
import src.models as models
from src import db
import requests
import re
import pdb
from datetime import datetime, timedelta
from src.models import position_location

class PositionBuilder:
    def __init__(self, card):
        self.card = card
        self.spans = None
        self.company_name = None

    def run(self):
        position = self.build_position()
        if not position.id:
            company = self.build_company()
            state = self.build_state()
            city = self.build_city()
            position.card = self.card
            company.positions.append(position)
            position_location = self.build_position_location(position, city,
             state, self.card.remote)
            position.title = self.card.title
            position.description = self.card.description
            position.date_posted = self.card.get_date_posted()
            
            salaries = self.card.get_salaries()
            if salaries:
                position.minimum_salary = salaries[0]
                position.maximum_salary = salaries[-1]
            experience_years = self.card.years_range()
            if experience_years:
                position.minimum_experience = experience_years[0]
                position.maximum_experience = experience_years[-1]
        return position
                
    def build_position_location(self, position, city, state, remote):
        position_location = models.PositionLocation()
        position_location.position = position
        position_location.city = city
        position_location.state = state
        position_location.is_remote = remote
        return position_location
        
        
    def build_city(self):
        city = self.get_or_build(db, models.City, name=self.card.city)
        return city

    def build_company(self):
        company = self.get_or_build(db, models.Company, name=self.card.company_name)
        return company

    def build_position(self):
        position = self.get_or_build(db, models.Position, source_id=self.card.source_id)
        return position

    def build_state(self):
        state = self.get_or_build(db, models.State, name=self.card.state)
        return state
        
    def get_or_build(self, db, model, **kwargs):
        instance = db.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            db.session.add(instance)
            return instance
