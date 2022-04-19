from src.adapters.indeed_client import get_page
from src.adapters.page_runner import PageRunner
from src.models import Scraping, ScrapedPage
from src import db

class ScrapingRunner():
    def previous_page(self):
        last_scraping = db.session.query(ScrapedPage).filter(ScrapedPage.scraping_id ==
         self.scraping.id).order_by(ScrapedPage.timestamp.desc()).first()
        
        if last_scraping:
            page_num = last_scraping.page_number
            return page_num

    def run_scraping(self, job_title, location, experience_level):
        
        scraping = Scraping(query_string = job_title, 
        location = location,
         experience_level = experience_level)
        db.session.add(scraping)
        self.scraping = scraping
        start = 0
        
        while scraping:
            page_html = get_page(job_title, location, 
            experience_level = experience_level, start = start)
            page_runner = PageRunner(page_html)
            
            scraped_page = page_runner.run(query = job_title)['scraped_page']
            
            previous_page_num = self.previous_page()
            
            start += 10
            self.scraping.scraped_pages.append(scraped_page)
            if previous_page_num == scraped_page.page_number: return scraping
            print('current page', scraped_page.page_number, 'previous page', previous_page_num)
            

    def page_scraper(job_title, location, start):
        page = get_page(job_title, location, start)
        # build scraped page
        # pass scraped page into page runner
