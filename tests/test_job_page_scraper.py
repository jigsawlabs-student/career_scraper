from bs4 import BeautifulSoup as bs
from src.models.scraped_page import *
import src.models as models
from tests.data.job_page import job_page


from src.adapters.job_page_scraper import JobPageScraper


f = open("./tests/data/readme.txt", "r")
page_html = f.read()

def test_get_title():    
    page_scraper = JobPageScraper(page_html = page_html)
    assert page_scraper.get_title() == 'Data Engineer'

def test_get_salaries():    
    page_scraper = JobPageScraper(page_html = page_html)
    page_scraper.get_salaries() 
    assert page_scraper.salaries == [130000, 200000]

def test_get_city_state():
    page_scraper = JobPageScraper(page_html = page_html)
    assert page_scraper.get_city_state() == ('New York', 'NY')

def test_get_description():
    page_scraper = JobPageScraper(page_html = page_html)
    text = """\n\n  As a member of the IT Data Analytics team, the Data Engineer's 
    responsibilities involve preparing data for analytical or operational uses, 
    typically building and maintaining data pipelines to pull together
     information from different sources; integrating, consolidating and cleansing data;
      and structuring it for use in individual analytics applications
       in a ready-to-use form to data scientists who are
        looking to run queries and algorithms against the information for predictive analytics,
      machine learning and data mining purposes.\n  \n
          The IT Data Analytics team as a whole is responsible for developing data solutions to support business decisions, directly or indirectly by providing raw / pre-processed data to Data Scientists and Traders. This is achieved with agile methodology and a lot of teamwork. Always oriented to delivery, the area fosters technical and business discussions seeking continuous improvement in results, with continuous advent of cutting-edge technology in Data Science, Cloud Computing, Clusterization, Containerization and Machine Learning. \n   \n\n\nWork Activities / Tasks\n\n\n Quick Ingestion of structured or unstructured data from new sources. Through scraping scripts, services, jobs, crawlers, ETL and streaming\n Data cleaning, enrichment or transformation using most appropriate tools for quick delivery and greater reuse\n Safe and efficient persistence of data via severals types of storage, such as DBs, warehouses, data lakes of different formats\n Data distribution / showcase through services or query interfaces for internal consumption\n Maintenance of existing data pipelines and databases\n Support on automation of post-processing routines when required, including prediction models and visualization\n Support to Data Scientists in use of common internal libraries in Python / R, cloud resources and access to existing data.\n Knowledge retention and maintenance of a KB about data sources and pipelines\n Development of new visualizations using data vis platforms\n Assist with business initiatives and projects  \n\nRequired Background\n\n\n\n\n Fluent in English\n Background in Engineering, Computer Science, Systems Analysis, Data Science, Information Systems\n Familiar with Python distributions, notebooks and IDEs (Anaconda, Jupyter, Spyder, PyCharm, etc.)\n Proficiency in scripting languages such as Python and R for Data Crawling, Parsing, etc. Master Pandas library\n Experience with AWS DB stack such as DynamoDB, Redshift and Aurora\n Knowledge of other common AWS resources (S3, Lambda, Athena, EMR, Faregate, Kinesis, EC2, API Gateway, CloudWatch)\n Proven experience with MS SQL database\n Experience with Containers.\n Knowledge of web formats (eg. html, json), and experience with web scraping. \nExperience with DevOps or GIT source code repository\n Use of IaC with AWS Cloud Formation\n Exposure to integration tools such as Rest API, Web API, Entity Framework, SSIS, WPF and WCF  \n\nBehavioral Competencies\n\n\n\n Logical reasoning\n Analytical capacity and organization\n Team Player\n Strongly Motivated\n High problem solving skills\n\n\n\n\n\n\n\n\n We offer flexibility with a 3 days working from the office and 2 days from home pattern\n Employee & family Health Care\n Pension / 401k match\n\n Interview with the Hiring Manager, the team, N+2 and HR. Specific tests may apply. Python, R, AWS, Jupyter, SQLGit, CloudFormation\n \n"""
    assert page_scraper.get_description()[:10] == text[:10]
    
def test_get_company_name():
    page_scraper = JobPageScraper(page_html = page_html)
    assert page_scraper.get_company_name() == 'Engelhart'

def test_get_date_posted():
    page_scraper = JobPageScraper(page_html = page_html)
    assert page_scraper.get_date_posted().day == 6




