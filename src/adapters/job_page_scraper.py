from bs4 import BeautifulSoup as bs
from datetime import datetime
import re
from datetime import datetime, timedelta

class JobPageScraper:
    def __init__(self, page_html = ''):
        self.page_html = page_html
        self.bs = bs(page_html)

    def pull_data(self):
        self.get_title()
        self.get_salaries()
        self.get_location()
        self.get_city_state()
        self.get_description()
        self.get_company_name()
        self.get_date_posted()
        self.years_range()
           
    def get_company_name(self):
        company_div = self.bs.find('div', {'class': "jobsearch-InlineCompanyRating"})
        if company_div:
            company_text = company_div.text
            self.company_name = company_text
        else:
            self.company_name = ''
        return self.company_name

    def get_title(self):
        title = self.bs.find('h1').text
        self.title = title
        return title

    def salary_text(self):
        salary_text_div = self.bs.find('div', id="salaryInfoAndJobType")
        if salary_text_div:
            return salary_text_div.text

    def get_salaries(self):
        salary_text = self.salary_text()

        if not salary_text:
            self.salaries = []
            return []
        salary_text = salary_text.split(' a ')[0]
        salary_text = salary_text.replace(',', '')
        salarie_ks =  re.findall(r'[0-9.]+K', salary_text)
        if salarie_ks:
            self.salaries = [int(float(salary.replace('K', '')) * 1000) 
            for salary in salarie_ks if 'K' in salary]
        else:
            salaries =  re.findall(r'\d+', salary_text)
            self.salaries = list(sorted([int(salary) for salary in salaries]))
        return self.salaries

    def get_description(self):
        self.description = self.bs.find(id='jobDescriptionText').text
        return self.description

    def salary_is_estimated(self):
        salary_text = self.salary_text()
        return 'estimated' in salary_text.lower()

    def salary_time_period(self):
        timeframes = ['year', 'month', 'hour', 'day']
        for timeframe in timeframes:
            if timeframe in self.salary_text().lower():
                return timeframe

    def get_location(self):
        location = self.bs.find('div', {"class": "jobsearch-JobInfoHeader-subtitle"})
        location = location.find_all('div')[-2]
        if location:
            location = location.text.lower()
            self.location_text = location
            self.remote = 'remote' in location
        return location
            

    def get_city_state(self):
        location = self.get_location()
        if 'remote' in location:
            self.city = 'remote'
            self.state = 'remote'
            return (self.city, self.state)
        split_text = location.split(', ')
        if len(split_text) > 1:
            city, state = split_text
            self.city = " ".join(re.findall("[a-zA-Z]+", city)).title()
            state_text = state.split(' ')[0:-1]
            self.state = re.findall("[a-zA-Z]+", state)[0].upper()
              
        else:
            self.city = 'NA'
            self.state = 'NA'
        return (self.city, self.state)

    def get_date_posted(self):
        days_ago = self.bs.find('div', {"class":
             "jobsearch-JobMetadataFooter"}).find_all('div')[1].text
        numbers = re.findall(r'^\D*(\d+)', days_ago)
        if numbers:
            date_posted = datetime.today() - timedelta(days=int(numbers[0]))
            self.date_posted = date_posted
        else:
            self.date_posted = datetime.today()
            date_posted = datetime.today()
        return date_posted
        
    def date_text(self):
        text = self.bs.find('span', {'class': 'date'}).text
        days_ago = re.findall(r'\d+', text)
        return days_ago

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