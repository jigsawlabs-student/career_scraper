from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from src import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
from src.adapters.indeed_client import get_card_from, get_page_from
from src.adapters.job_page_scraper import JobPageScraper
import re

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.String)
    html = db.Column(db.Text)
    scraped_page_id = db.Column(db.Integer, db.ForeignKey('scraped_pages.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    position = relationship("Position", back_populates="card")
    scraped_page = relationship("ScrapedPage", back_populates="cards")

    @classmethod
    def build_card_from(self, card_html):
        card = Card()
        card.set_html(card_html)
        if card.is_card():
            card.pull_data()
            return card
        else:
            job_id = card.bs['id'].split('_')[1]
            page_scraper = self.build_page_scraper_for(job_id)
            card = self.build_card(page_scraper)
            return card

    def is_card(self):
        location = self.bs.find('div', {"class": "companyLocation"})
        return location

    @classmethod
    def build_card(self, page_scraper):
        card = Card()
        card.source_id = page_scraper.source_id
        card.title = page_scraper.title
        card.salaries = page_scraper.salaries
        card.description = page_scraper.description
        card.state = page_scraper.state
        card.city = page_scraper.city
        card.date_posted = page_scraper.date_posted
        card.company_name = page_scraper.company_name
        card.remote = page_scraper.remote
        card.years = page_scraper.years
        return card
        
    @classmethod
    def build_page_scraper_for(self, id):
        html = get_page_from(id)
        page_scraper = JobPageScraper(page_html = html)
        page_scraper.source_id = id 
        page_scraper.pull_data()
        return page_scraper
        

    def pull_data(self):
        self.set_html(self.html)
        self.get_source_id()
        self.get_title()
        self.get_salaries()
        self.get_description()
        self.get_location()
        self.get_city_state()
        self.get_company_name()
        self.get_date_posted()
        self.years_range()

    @orm.reconstructor
    def init_on_load(self):
        self.bs = self.pull_data()

    def set_html(self, html):
        self.html = str(html)
        self.bs = bs(str(html), "html.parser").find('a')
        return html

    def find_years_text(self):
        descr = self.description
        year_results = re.finditer('year', descr)

        
        
        indices = [result.start() for result in year_results]
        # potentially find digit - digit pattern, or digit+ pattern
        year_texts =  [descr[i - 50:i + 50] for i in indices]
        yr_results = re.finditer('yr', descr)
        yr_indices = [result.start() for result in yr_results]
        yr_texts =  [descr[i - 50:i + 50] for i in yr_indices]
        return year_texts + yr_texts

    def years_range(self):
        texts = self.find_years_text()
        if texts:
            together = ' '.join(texts)
            found_years = re.findall(r'[0-9.-]+', together)
            all_years = ' '.join([year.replace('-', ' ') for year in found_years])
            collected_years = re.findall(r'[0-9]+', all_years)
            ordered_years = sorted([int(year) for year in collected_years])
            trimmed_years = [year for year in ordered_years if year < 11]
            if trimmed_years:
                years = [trimmed_years[0], trimmed_years[-1]]
                self.years = years
                return years
            else:
                self.years = []
                return self.years
        else:
            self.years = []
            return self.years
                

    def date_text(self):
        text = self.bs.find('span', {'class': 'date'}).text
        return text

    def get_date_posted(self):
        days_ago = self.date_text()
        if not days_ago:
            breakpoint()
        numbers = re.findall(r'^\D*(\d+)', days_ago)
        if numbers:
            date_posted = datetime.today() - timedelta(days=int(numbers[0]))
            self.date_posted = date_posted
        else:
            self.date_posted = datetime.today()
            date_posted = datetime.today()
        return date_posted
        


    def get_source_id(self):
        self.source_id = self.bs['data-jk']
        return self.source_id

    def get_title(self):
        job_title_h2 = self.bs.find('h2', {'class': 'jobTitle'})
        if job_title_h2:
            self.title = job_title_h2.text.split('(')[0].strip()
            cap_letters = [i for i in range(len(self.title)) if self.title[i].isupper()]
            if cap_letters:
                first_cap = cap_letters[0]
                self.title = self.title[first_cap:]
            return self.title
        else:
            self.title = self.bs.find('span').text
            return self.title

    def salary_text(self):
        salary_texts = self.bs.find_all('div', {"class": "salaryOnly"})
        if not salary_texts: return ''
        salary_text = salary_texts[0].text
        return salary_text

    def get_salaries(self):
        salary_text = self.salary_text().split(' a ')[0]
        if not salary_text: 
            self.salaries = []
            return []
        salary_text = salary_text.replace(',', '')
        salarie_ks =  re.findall(r'[0-9.]+K', salary_text)
        if salarie_ks:
            self.salaries = [int(float(salary.replace('K', '')) * 1000) 
            for salary in salarie_ks if 'K' in salary]
        else:
            salaries =  re.findall(r'\d+', salary_text)
            self.salaries = list(sorted([int(salary) for salary in salaries]))
        return self.salaries

    def salary_is_estimated(self):
        salary_text = self.salary_text()
        return 'estimated' in salary_text.lower()

    def salary_time_period(self):
        timeframes = ['year', 'month', 'hour', 'day']
        for timeframe in timeframes:
            if timeframe in self.salary_text().lower():
                return timeframe

    def job_term(self):
        terms = ['full-time', 'part-time', 'contract', 'hourly']
        for term in terms:
            if term in self.salary_text().lower():
                return term

    def get_description(self):
        id = self.get_source_id()
        self.description = get_card_from(id)[id]
        return self.description

    def get_location(self):
        location = self.bs.find('div', {"class": "companyLocation"})
        if location:
            location = location.text.lower()
            self.location_text = location
            self.remote = 'remote' in location
            return location
        else:
            return 'NA'
        
    def get_city_state(self):
        location = self.get_location()
        split_text = location.split(', ')
        if len(split_text) > 1:
            city, state = split_text
            self.city = " ".join(re.findall("[a-zA-Z]+", city)).title()
            state_text = state.split(' ')[0:-1]
            self.state = re.findall("[a-zA-Z]+", state)[0].upper()
        else: 
            text = self.bs.find('div', {"class":
             "jobsearch-JobInfoHeader-subtitle"})
            if text:
                text.text.lower()
                if 'remote' in text:
                    self.city = 'remote'
                    self.state = 'remote'
            else:
                self.city = 'NA'
                self.state = 'NA'
        return (self.city, self.state)

    def get_company_name(self):
        company_name = self.bs.find_all('span', {"class": "companyName"})
        if company_name:
            self.company_name = company_name[0].text
        else:
            self.company_name = ''
        return self.company_name


    