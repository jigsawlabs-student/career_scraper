from src.adapters.indeed_client import *
import src.models as models
from src import db
import requests
import re
import pdb

from src.models import position_location

class IndeedAdapter:
    def __init__(self, card):
        self.card = card
        self.spans = None
        self.company_name = None
        
        
    def pull_data(self):
        self.get_spans()
        self.source_id = self.get_source_id()
        self.title = self.get_title()
        self.salaries = self.get_salaries()
        self.description = self.get_description()
        self.location = self.get_location()
        self.city, self.state = self.get_city_state()
        self.company_name = self.get_company_name()

    def build_models(self):
        position = self.build_position()
        if not position.id:
            company = self.build_company()
            state = self.build_state()
            city = self.build_city()
            position_location = self.build_position_location(position, city,
             state, self.remote)
            company.positions.append(position)
            position.position_locations.append(position_location)
            db.session.commit()
        return position
            


    def build_position_location(self, position, city, state, remote):
        position_location = models.PositionLocation()
        position_location.position = position
        position_location.city = city
        position_location.state = state
        position_location.is_remote = remote
        
        
    def build_city(self):
        city = self.get_or_build(db, models.City, name=self.city)
        return city

    def build_company(self):
        company = self.get_or_build(db, models.Company, name=self.company_name)
        return company

    def build_position(self):
        position = self.get_or_build(db, models.Position, source_id=self.source_id)
        return position

    def build_state(self):
        state = self.get_or_build(db, models.State, name=self.name)
        return state
        

    def get_spans(self):
        self.spans = self.spans or self.card.findAll('span')
        return self.spans

    def get_source_id(self):
        self.id = self.card['data-jk']
        return self.id

    def get_title(self):
        self.title = self.card.find('h2', {'class': 'jobTitle'}).text.split('(')[0].strip()
        return self.title

    def get_salaries(self):
        salary_text = self.card.find_all('div', {"class": "salaryOnly"})[0].text
        salary_text = salary_text.replace(',', '')
        salaries =  re.findall(r'\d+', salary_text)
        
        self.salaries = list(sorted([int(salary) for salary in salaries]))
        return self.salaries

    def get_description(self):
        id = self.get_id()
        self.description = get_card_from(id)[id]
        return self.description

    def get_location(self):
        location = self.card.find('div', {"class": "companyLocation"}).text.lower()
        self.location_text = location
        self.remote = 'remote' in location
        if self.remote:
            location = location.replace('remote', '')
        return location


    def get_city_state(self):
        location = self.get_location()
        split_text = location.split(', ')
        if len(split_text) > 1:
            city, state = split_text
            city_text = city.split(' ')[-1]
            self.city = " ".join(re.findall("[a-zA-Z]+", city_text)).capitalize()
            state_text = state.split(' ')[0]
            self.state = " ".join(re.findall("[a-zA-Z]+", state_text)).upper()
            return (self.city, self.state)
        else: 
            return ('NA', 'NA')

    def get_company_name(self):
        self.company_name = self.company_name or self.card.find_all('span', {"class": "companyName"})[0].text
        return self.company_name

    def get_or_build(db, model, **kwargs):
        instance = db.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            db.session.add(instance)
            return instance
        

    
