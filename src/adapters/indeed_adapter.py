from src.adapters.indeed_client import *
from src.models.position import Position
import requests
import re
import pdb

class IndeedAdapter:
    def __init__(self, card):
        self.card = card
        self.spans = None
        self.company_name = None
        
        
    def run(self):
        self.get_spans()
        id = self.get_id()
        title = self.get_title()
        salaries = self.get_salaries()
        description = self.get_description()
        location = self.get_location()
        city, state = self.get_city_state()
        company_name = self.get_company_name()
        position = Position(id, title, salaries, description, city, state, company_name, location_text = self.location_text, remote = self.remote)
        return position
        

    def get_spans(self):
        self.spans = self.spans or self.card.findAll('span')
        return self.spans

    def get_id(self):
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
            self.city = city.split(' ')[-1].capitalize()
            self.state = state.split(' ')[0].upper()
            
            return (self.city, self.state)
        else: 
            return ('NA', 'NA')

    def get_company_name(self):
        self.company_name = self.company_name or self.card.find_all('span', {"class": "companyName"})[0].text
        return self.company_name
        

    
